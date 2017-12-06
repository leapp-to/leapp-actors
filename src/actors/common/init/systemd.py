from os.path import basename
from collections import defaultdict
from json import dumps

import leapp


try:
    import dbus
except ImportError:
    leapp.bail(leapp.Severity.Fatal,
               'unable to obtain list of systemd services - no dbus library')


def asdict(obj):
    mapping = getattr(obj, '_mapping', [])
    return {k: getattr(obj, k) for k in mapping}


class SystemdUnitFile(object):
    ''' Object representing a unit file, which contains a description
        of one or more `SystemdUnit` units
    '''
    _mapping = ('path', 'name', 'status', 'type')

    def __init__(self, unit, unit_status):
        self.path = unit
        self.name = basename(unit)
        self.status = unit_status
        self.type = self.name.split('.')[1]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class SystemdUnit(object):
    ''' Basic representation of `SystemdUnit` used to encapsulate services

    '''
    _mapping = ('unit_name', 'description', 'load_state', 'active_state', 'sub_state',
                'followers', 'object_path', 'job_id', 'job_type', 'job_object')

    def __init__(self, unit, exec_start, env):
        self.exec_start = exec_start
        self.environment = env
        for i, v in enumerate(self._mapping):
            setattr(self, v, unit[i])


class SystemdDBusAnalyzer(object):
    ''' Figure information about units and and unit files from
        systemd via DBus

    '''
    def __init__(self):
        self._bus = dbus.SystemBus()
        obj = self._bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        self._interface = dbus.Interface(obj, 'org.freedesktop.systemd1.Manager')

    def __del__(self):
        if self._bus and self._bus.get_is_connected():
            self._bus.close()
            del self._bus

    def run(self):
        units, unit_files = [], []

        for unit in self._interface.ListUnits():
            #
            # Sixth element of the Unit is *ObjectPath*
            service = self._bus.get_object('org.freedesktop.systemd1', unit[6])
            proxy = dbus.Interface(service, dbus_interface='org.freedesktop.DBus.Properties')
            try:
                exec_start = proxy.Get('org.freedesktop.systemd1.Service', 'ExecStart')
                if exec_start:
                    #
                    # First element contains argv[] of the unit
                    exec_start = exec_start[0][1]
                env = proxy.Get('org.freedesktop.systemd1.Service', 'Environment')
            except dbus.exceptions.DBusException as de:
                exec_start, env = None, None
                if de.get_dbus_name() != 'org.freedesktop.DBus.Error.UnknownProperty':
                    raise de
            units.append(SystemdUnit(unit, exec_start, env))

        for unit, status in self._interface.ListUnitFiles():
            unit_files.append(SystemdUnitFile(unit, status))

        return (units, unit_files)


def collect_related_units(units, unit_files):
    ''' Put together (zip) one or more units originating from a respective unit file

        :type units: list[SystemdUnit]
        :type unit_files: list[SystemdUnitFile]
        :return:
    '''

    coalesced = defaultdict(list)

    def _find_unit_file(name, startswith=False):
        for uf in unit_files:
            if not startswith and uf.name == name:
                return uf
            elif startswith and uf.name.startswith(name):
                return uf

        return None

    # We treat `units` as our point of reference since:
    # 1) Not every unit has associated unit file (systemd-run etc.)
    # 2) Unit file can be parent of multiple units
    #
    # Units that have no unit files will be located under the `None` key
    for unit in units:
        name = unit.unit_name
        at_sign = unit.unit_name.find('@')
        has_at_sign = at_sign > -1
        if has_at_sign:
            name = unit.unit_name[0:at_sign]
        unit_file = _find_unit_file(name, startswith=has_at_sign)
        coalesced[unit_file].append(unit)

    for uf in unit_files:
        if uf not in coalesced:
            coalesced[uf] = []

    return coalesced


def remap_as_dictionary(related):
    ''' Convert our data into simple dictionaries that
        can be output as json

    '''
    result = {'transient': None, 'unit_files': []}

    for unit_file, units in related.items():
        if not unit_file and units:
            result['transient'] = [asdict(u) for u in units]
        else:
            u = [asdict(u) for u in units]
            result['unit_files'].append(
                {'unit_file': asdict(unit_file), 'units': u}
            )

    return result


def get_service_data():
    analyzer = SystemdDBusAnalyzer()
    units, unit_files = analyzer.run()
    related = collect_related_units(units, unit_files)
    return remap_as_dictionary(related)


print(dumps(get_service_data()))