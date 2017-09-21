import json
import rpm


def format_version(app):
    return '{e}:{v}-{r}.{a}'.format(e=app['epoch'] or 0,
                                    v=app['version'],
                                    a=app['arch'],
                                    r=app['release'])


print json.dumps({
    'rpm_packages': [{'name': app['name'],
                      'version': format_version(app)}
                     for app in rpm.ts().dbMatch()]})
