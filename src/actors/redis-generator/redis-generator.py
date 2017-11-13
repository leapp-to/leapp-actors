import sys
import json
import shlex

from subprocess import Popen, PIPE


def _execute(cmd):
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    out, _ = proc.communicate()
    if proc.returncode != 0:
        raise Exception("Command failed")
    return out.strip()


def _create_redis_container(redis):
    cname = _execute('buildah from redis:{0}-alpine'.format(redis['version']))
    if not cname:
        raise Exception('Error creating container')
    return cname


def _copy_to_container(cname, src, dst):
    if cname and src and dst:
        _execute('buildah copy {0} {1} {2}'.format(cname, src, dst))


def _get_container_id(cname):
    cntrs = json.loads(_execute('buildah containers --json'))
    ids = (x['id'].strip() for x in cntrs if x['containername'] == cname)
    try:
        cntr_id = next(ids)
    except StopIteration:
        raise Exception('There is more than one container with the same cname')
    else:
        return cntr_id.strip()


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
    _execute('buildah commit --creds {user}:{password} {container_id} {uri}'.format(
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
