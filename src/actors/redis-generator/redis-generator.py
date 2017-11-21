import os
import sys
import json
import shlex
import subprocess
from distutils.spawn import find_executable


def find_buildah():
    def _is_valid(path):
        return path and os.path.isfile(path) and os.access(path, os.X_OK)
    path = os.path.abspath('buildah')
    if not _is_valid(path):
        path = find_executable('buildah')
    if not _is_valid(path):
        raise Exception('Could not find a valid buildah binary: {0}'.format(path))
    return path


BUILDAH = find_buildah()


def _execute(cmd):
    out = subprocess.check_output(shlex.split(cmd))
    return out.strip()


def _create_redis_container(redis):
    # TODO: use a RHEL/CentOS-based image
    cname = _execute('{buildah} from redis:{version}-alpine'.format(
        buildah=BUILDAH,
        version=redis['version'])
    )
    if not cname:
        raise Exception('Error creating container')
    return cname


def _copy_to_container(cname, src, dst):
    if cname and src and dst:
        _execute('{buildah} copy {cname} {src} {dst}'.format(
            buildah=BUILDAH,
            cname=cname,
            src=src,
            dst=dst
        ))


def _get_container_id(cname):
    cntrs = json.loads(_execute('{buildah} containers --json'.format(buildah=BUILDAH)))
    ids = [x['id'].strip() for x in cntrs if x['containername'] == cname]
    if len(ids) != 1:
        raise Exception('Incorrect number of containers with name {0}'.format(cname))
    return ids[0]


def _join_docker_uri(registry, cname):
    # TODO: workaround to bypass urljoin's inability to work with docker:// schemas
    return '/'.join([registry['address'].strip('/'), cname.strip('/')])


if __name__ == "__main__":
    inputs = json.load(sys.stdin)
    redis = inputs['redis'][0]['value']
    registry = inputs['registry'][0]['value']

    # Create container
    cname = _create_redis_container(redis)
    _copy_to_container(cname, redis.get('config_file_path'), '/etc/redis.conf')
    _copy_to_container(cname, redis.get('db_file_path'), '/data/dump.rdb')

    # Gather info to create and push image
    cntr_id = _get_container_id(cname)
    uri = _join_docker_uri(registry, cname)

    # Create image out of the container and push it to the registry
    _execute('{buildah} commit --creds {user}:{password} {container_id} {uri}'.format(
        buildah=BUILDAH,
        user=registry['user'],
        password=registry['password'],
        container_id=cntr_id,
        uri=uri,
    ))

    print(json.dumps({
        'generated_redis_image_uri': [{
            'value': uri
        }]
    }))
