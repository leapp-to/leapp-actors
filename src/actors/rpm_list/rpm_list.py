import json
import rpm
import sys


def format_version(app):
    return '{e}:{v}-{r}.{a}'.format(e=app['epoch'] or 0,
                                    v=app['version'],
                                    a=app['arch'],
                                    r=app['release'])


sys.stdout.write(json.dumps({
    'rpm_packages': {
        'packages': [{'name': app['name'],
                      'version': format_version(app)}
                     for app in rpm.ts().dbMatch()]}}) + '\n')
