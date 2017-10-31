#!/usr/bin/env python
import psutil
import socket
import nmap
import json
import sys
from util import PortList


class PortScanException(Exception):
    pass


def port_scan(ip_or_fqdn, port_range=None, shallow=False, force_nmap=False):
    def _nmap(port_list, ip, port_range=None, shallow=False):
        if shallow and port_range is None:
            port_range = '{}-{}'.format(PortList.MIN_PORT, PortList.MAX_PORT)
        scan_args = '-sS' if shallow else '-sV'

        port_scanner = nmap.PortScanner()
        port_scanner.scan(ip, port_range, scan_args)
        scan_info = port_scanner.scaninfo()

        if scan_info.get('error', False):
            raise PortScanException(
                scan_info['error'][0] if isinstance(scan_info['error'], list) else scan_info['error']
            )

        for proto in port_scanner[ip].all_protocols():
            for port in sorted(port_scanner[ip][proto]):
                if port_scanner[ip][proto][port]['state'] in ('open', 'filtered'):
                    port_list.set_port(proto, port, port_scanner[ip][proto][port])
        return port_list

    def _net_util(port_list):
        sconns = psutil.net_connections(kind=port_list.PROTO_TCP)
        for sconn in sconns:
            addr, port = sconn.laddr
            if not port_list.has_port(port_list.PROTO_TCP, port):
                if sconn.pid:
                    name = psutil.Process(sconn.pid).name()
                else:
                    name = "Unknown"

            port_list.set_port(port_list.PROTO_TCP, port, {"name": name})
        return port_list

    port_list = PortList()

    if ip_or_fqdn in ('localhost', '127.0.0.1') and not force_nmap:
        return _net_util(port_list)

    ip = socket.gethostbyname(ip_or_fqdn)
    return _nmap(port_list, ip, port_range, shallow)


if __name__ == '__main__':
    inputs = json.load(sys.stdin)

    keys = {
        'host': 'host',
        'output': 'port_scan_result',
        'options': 'scan_options'}
    for arg in sys.argv[1:]:
        try:
            akey, value = arg.split('=')
            keys[akey] = value
        except ValueError:
            pass

    # Required
    host = inputs[keys["host"]][0].get("value")
    options = inputs.setdefault(keys["options"], [{}])[0]
    # Optional
    shallow = options.get("shallow_scan", True)
    force_nmap = options.get("force_nmap", False)
    port_range = options.get("port_range", None)

    # Set port_range to None if it is empty string or null in input JSON
    if not port_range:
        port_range = None

    port_list = PortList()
    result = port_scan(host, shallow=shallow, force_nmap=force_nmap, port_range=port_range)
    for ports in result.values():
        for item in ports.values():
            remove = [key for key in item.keys() if key not in ("name", "product")]
            for key in remove:
                del item[key]
    print(json.dumps({keys["output"]: [result]}))
