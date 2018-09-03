from openshift.common import osv3
from leapp import get_actor_input
from json import dumps


os_user, os_pw, login_url = get_actor_input('openshift_cluster_information')
osv3.oc(['login', '-u', os_user, '-p', os_pw, login_url])
token = osv3.oc(['whoami', '--token'])

print(dumps({'token': token}))