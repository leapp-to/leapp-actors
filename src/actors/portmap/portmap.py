#!/usr/bin/env python
from sets import Set
from json import dumps, load
from util import PortList
from util import PortMap
import sys


class PortCollisionException(Exception):
    pass


def map_ports(source_ports, target_ports, user_mapped_ports=None, user_excluded_ports=None):
    """
    :param source_ports:        ports found by the tool on source machine
    :param source_ports:        PortList
    :param target_ports:        ports found by the tool on target machine
    :param target_ports:        PortList
    :param user_mapped_ports:   port mapping defined by user
                                if empty, only the default mapping will aaplied

                                DEFAULT RE-MAP:
                                    22/tcp -> 9022/tcp
    :type user_mapped_ports:    PortMap
    :param user_excluded_ports: excluded port mapping defined by user
    :type user_excluded_ports:  PortList
    """

    user_mapped_ports = user_mapped_ports or PortMap()
    user_excluded_ports = user_excluded_ports or PortList()

    remapped_ports = []

    # add user ports which was not discovered
    for protocol in user_mapped_ports.get_protocols():
        for port in user_mapped_ports.list_ports(protocol):
            for user_target_port in user_mapped_ports.get_port(protocol, port):
                if target_ports.has_port(protocol, user_target_port):
                    raise PortCollisionException("Specified mapping is in conflict with target "
                                                 "{} -> {}".format(port, user_target_port))

            # Add dummy port to sources
            if not source_ports.has_port(protocol, port):
                source_ports.set_port(protocol, port)

    # Static (default) mapping applied only when the source service is available
    if not user_mapped_ports.has_tcp_port(22):
        user_mapped_ports.set_tcp_port(22, 9022)

    # remove unwanted ports
    for protocol in user_excluded_ports.get_protocols():
        for port in user_excluded_ports.list_ports(protocol):
            if source_ports.has_port(protocol, port):
                # remove port from sources
                source_ports.unset_port(protocol, port)

    # remap ports
    for protocol in source_ports.get_protocols():
        for port in source_ports.list_ports(protocol):
            source_port = port

            # remap port if user defined it
            if user_mapped_ports.has_port(protocol, port):
                user_mapped_target_ports = user_mapped_ports.get_port(protocol, port)
            else:
                user_mapped_target_ports = Set([port])

            for target_port in user_mapped_target_ports:
                while target_port <= PortList.MAX_PORT:
                    if target_ports.has_port(protocol, target_port):
                        if target_port == PortList.MAX_PORT:
                            raise PortCollisionException("Automatic port collision resolve failed, please use "
                                                         "--tcp-port SELECTED_TARGET_PORT:{} to solve the "
                                                         "issue".format(source_port))

                        target_port = target_port + 1
                    else:
                        break

                # add newly mapped port to target ports so we can track collisions
                target_ports.set_port(protocol, target_port)

                # create mapping array
                remapped_ports.append({
                    "protocol": protocol,
                    "port": source_port,
                    "exposed_port": target_port
                })

    return remapped_ports


def from_user(user_mapping):
    mapping = {}
    for entry in user_mapping.get("ports", ()):
        item = mapping.get(entry["port"], [])
        item.append(entry["port"])
        mapping[entry["port"]] = item
    return {key: list(set(value)) for key, value in mapping.items()}


if __name__ == '__main__':
    inputs = load(sys.stdin)

    # Required arguments
    src_dict = inputs["source_system_ports"]
    tgt_dict = inputs["target_system_ports"]

    # Optional arguments
    usr_dict = inputs.get("tcp_ports_user_mapping", {})
    exc_dict = inputs.get("excluded_tcp_ports", {})

    src = PortList(src_dict)
    tgt = PortList(tgt_dict)
    exc = PortList(exc_dict)
    usr = PortMap(from_user(usr_dict))

    print(dumps({"exposed_ports": {"ports": map_ports(src, tgt, usr, exc)}}))
