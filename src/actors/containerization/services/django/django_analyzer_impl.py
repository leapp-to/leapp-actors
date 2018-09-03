''' Leapp Django actor  '''

import ast
from subprocess import check_output
from json import loads, dumps
from os.path import dirname, join
from os import walk

import astor

SCAN_CODE = """
import subprocess, os, sys

inject = '''
import os, json
l, g = dict(), dict()
getter = \"\"\"
import {{module}}
DB=getattr({{module}}, 'DATABASES', dict())
CACHE=getattr({{module}}, 'CACHES', dict())
\"\"\"
mod = os.environ['DJANGO_SETTINGS_MODULE']
exec(compile(getter.format(module=mod), '<generated>', 'exec'), g, l)
os.write({write}, json.dumps(dict(db=l['DB'],
                                  cache=l['CACHE']), indent=4))
os.close({write})
'''

target = None
if len(sys.argv) > 2:
    print('Invalid invocation: django_analyzer.py [MANAGE_PY]')
    exit(-1)
elif len(sys.argv) == 1:
    target = 'manage.py'
else:
    target = sys.argv[1]


r, w = os.pipe()
pid = os.fork()
if pid > 0:
    os.close(r)
    p = subprocess.Popen(['python', target, 'shell'], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
    p.communicate(inject.format(write=str(w)))
    os.close(w) # Popen forks underneath so we need to close `w` here as well
    os.wait()
else:
    os.close(w)
    while True:
        data = os.read(r, 1024)
        if not data:
            break
        print(data)
"""

def generate_import_os():
    """ Generates `import os` statement

    """
    return ast.Import(
        names=[ast.alias(name='os', asname=None)]
    )


def check_os_imports(tree):
    """ Inspect top level import for `import os`

    """
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == 'os':
                    return True
        #TODO: Add support for from .. import ... and aliased imports
        #elif isinstance(node, ast.ImportFrom):
        #    if node.module == 'os':
        #        for name in node.names:
        #            if name.name == 'getenv' and name.asname is None:
        #                return True

    return False


def generate_host_var(service_name, default, var_prefix):
    """ Generate code for parsing service information from env. variables
        into a single variable:

            {var_prefix}_HOST - ip:port

        Note that this code currently skips the initial part of the content
        of the env. variable - either 'udp://' or 'tcp://', which,
        in terms of *service discovery* is just a noise.

    """
    return ast.Assign(
        targets=[
            ast.Name(id=var_prefix + '_HOST')
        ],
        value=ast.Subscript(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='os'),
                    attr='getenv'
                ),
                args=[ast.Str(s=service_name), ast.Str(s=default)],
                keywords=[],
                starargs=None,
                kwargs=None
            ),
            slice=ast.Slice(lower=ast.Num(n=6), upper=None, step=None)
        )
    )


def generate_host_port_vars(service_name, default, var_prefix):
    """ Generate code for parsing service information from env. variables
        into two variables:

            {var_prefix}_HOST - containing the IP/Hostname
            {var_prefix}_PORT - containing the Port

        Note that this code currently skips the initial part of the content
        of the env. variable - either 'udp://' or 'tcp://', which,
        in terms of *service discovery* is just a noise.

    """
    return ast.Assign(
        targets=[
            ast.Tuple(elts=[
                ast.Name(id=var_prefix + '_HOST'),
                ast.Name(id=var_prefix + '_PORT')
            ])
        ],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Subscript(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id='os'),
                            attr='getenv'
                        ),
                        args=[ast.Str(s=service_name), ast.Str(s=default)],
                        keywords=[],
                        starargs=None,
                        kwargs=None
                    ),
                    slice=ast.Slice(lower=ast.Num(n=6), upper=None, step=None)
                ),
                attr='rsplit'
            ),
            args=[ast.Str(s=':'), ast.Num(n=1)],
            keywords=[],
            starargs=None,
            kwargs=None
        )
    )


def find_key(keys, key):
    """ Find index of string `key` in `keys`, and only take into
        account string keys, not arbitrary stuff overriding the
        `__hash__` method

    """
    for i, k in enumerate(keys):
        # We can only work with string based keys
        # for now
        if not isinstance(k, ast.Str):
            continue
        if k.s == key:
            return i


class ValueEnvTransformer(ast.NodeTransformer):
    """ AST Transformer to turn immediate string value into
        a variable reference

    """
    def __init__(self, key, default):
        self.key = key
        self.default = default

    def visit_Str(self, node):
        return ast.copy_location(
            ast.Name(id=self.key),
            node
        )


class AssignInspector(ast.NodeVisitor):
    """ Inspect assignemt to variable `var_name` and figure
        out if the RHS is a dictionary with "default" key,
        the value of which is another dictionary with a key
        specified in `find`, and replace that value with variable
        name specified in `env_replace` using `default` for default
        value if there's no env. variable with the specified name

    """
    def __init__(self, var_name, find, env_replace, default):
        self.find = find
        self.env_replace = env_replace
        self.default = default
        self.var_name = var_name

    def visit_Assign(self, node):
        children = list(ast.iter_child_nodes(node))
        if isinstance(children[1], ast.Dict) and children[0].id == self.var_name:
            dict_ = children[1]
            idx = find_key(dict_.keys, 'default')
            if idx is None:
                return
            dict_ = dict_.values[idx]
            idx = find_key(dict_.keys, self.find)
            transformer = ValueEnvTransformer(self.env_replace, self.default)
            dict_.values[idx] = transformer.visit(dict_.values[idx])


def process_settings_file(file_path):
    " Process Django settings file "
    tree = ast.parse(open(file_path, 'r').read())
    visitors = [
        # Transform configuration keys in DATABASES
        AssignInspector('DATABASES', 'HOST', 'OPENSHIFT_PGSQL_HOST', ''),
        AssignInspector('DATABASES', 'PORT', 'OPENSHIFT_PGSQL_PORT', ''),
        # Transform configuration keys in CACHES
        AssignInspector('CACHES', 'LOCATION', 'OPENSHIFT_MEMCACHED_HOST', '127.0.0.1:11211')
    ]

    for visitor in visitors:
        visitor.visit(tree)

    nodes = []
    if not check_os_imports(tree):
        nodes.append(generate_import_os())
    nodes.append(generate_host_port_vars('PGSQL_SERVICE_SERVICE', 'tcp://127.0.0.1:5432', 'OPENSHIFT_PGSQL'))
    nodes.append(generate_host_var('MEMCACHED_SERVICE_SERVICE', 'tcp://127.0.0.1:11211', 'OPENSHIFT_MEMCACHED'))

    tree.body = nodes + tree.body

    return astor.to_source(tree)


def any_endswith(seq, string):
    " Find if any item in `seq` ends with `string` "
    if not seq:
        return False
    return any(s.endswith(string) for s in seq)


def first_endswith(seq, string):
    " Find the first  item in `seq` that ends with `string` "
    for item in seq:
        if item.endswith(string):
            return item


def any_contains(seq, string):
    " Find if any item in `seq` contains `string` "
    if not seq:
        return False
    return any(string in s for s in seq)


def first_contains(seq, string):
    " Find the first  item in `seq` that contains `string` "
    if not seq:
        return None
    for item in seq:
        if string in item:
            return item


__comparator_map = {
    'any_endswith': any_endswith,
    'any_contains': any_contains,
}


def find_unit_by(units, key, value, selector=None, comparator=None, lowercase=False):
    """

    :param units: 
    :type units: map[systemd.Unit, systemd.UnitFile]
    :param key: 
    :type key: str or any
    :param value: 
    :param selector: 
    :type selector: func
    :param comparator: 
    :type comparator: func
    :param lowercase: 
    :type lowercase: bool
    :return: 
    """
    for uf in units['unit_files']:
        for unit in uf['units']:
            k = unit[key] if not selector else selector(unit)
            if not selector and lowercase:
                k = k.lower()
            if comparator:
                if comparator(k, value):
                    yield unit
            elif value in k:
                yield unit


def find_postgresql_units(units):
    return find_unit_by(units, 'unit_name', 'postgresql', lowercase=True)


def find_django_units(units):
    return find_unit_by(units, 'exec_start', 'manage.py', comparator=any_contains)


def find_memcached_units(units):
    return find_unit_by(units, 'unit_name', 'memcached', lowercase=True)


def get_service_data():
    return {'unit_files': []}


def find_pgdata(pgsql_unit):
    key = 'PGDATA='
    vars = pgsql_unit['environment']
    for var in vars:
        if var.startswith(key):
            return var[len(key):]


def find_settings_files(base_path):
    for root, dirs, files in walk(base_path):
        for file in files:
            if 'local_setting' in file and file[-3:] == '.py':
                yield join(root, file)


def analyze_django_units(units):
    analyzed_units = []
    for unit in units:
        manage_py = first_contains(unit['exec_start'], 'manage.py')
        data = check_output(['python', 'django_analyzer.py', manage_py])
        data_dir = dirname(manage_py)
        settings = list(find_settings_files(data_dir))
        analyzed_units.append({
            'unit': unit,
            'data': loads(data),
            'path': data_dir,
            'settings': settings,
            'deploy_settings': [
                {
                    'name': s,
                    'detail': process_settings_file(s)
                } for s in settings
            ]
        })
    return analyzed_units


service_data = get_service_data()
django_units = list(find_django_units(service_data))
postgres_units = list(find_postgresql_units(service_data))
memcached_units = list(find_memcached_units(service_data))

data = {
    'django': analyze_django_units(django_units),
    'detail': {}
}
data['detail']['memcached'] = {
    'detail': memcached_units,
    'data_dirs': []
}
data['detail']['postgresql'] = {
    'detail': postgres_units,
    'data_dirs': list({find_pgdata(pu) for pu in postgres_units})
}

from shutil import copyfile
for dju in data['django']:
    ds = dju['deploy_settings'][0]
    with open('artifacts/local_settings.py', 'w+') as out:
        out.write(ds['detail'])
    copyfile(ds['name'], 'artifacts/local_settings.py.original')

print(dumps(data, indent=4))
