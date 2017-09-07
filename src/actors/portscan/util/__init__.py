class PortList(dict):
    PROTO_TCP = "tcp"
    PROTO_UDP = "udp"

    MIN_PORT = 1
    MAX_PORT = 65535

    def __init__(self, src=None):
        super(PortList, self).__init__()

        self[self.PROTO_TCP] = {}
        self[self.PROTO_UDP] = {}

        # Copy dict to PortList
        if src:
            for proto in self.PROTO_TCP, self.PROTO_UDP:
                if proto in src.keys():
                    for port, data in src[proto].items():
                        self.set_port(proto, port, data)

    def _raise_for_protocol(self, protocol):
        if protocol not in self.get_protocols():
            raise ValueError("Invalid protocol: {}".format(str(protocol)))

    def set_port(self, protocol, source, data=None):
        self._raise_for_protocol(protocol)

        if int(source) >= self.MIN_PORT and int(source) <= self.MAX_PORT:
            self[protocol][int(source)] = data
        else:
            raise ValueError("Port must be in interval <{}; {}>".format(self.MIN_PORT, self.MAX_PORT))

    def set_tcp_port(self, source, target=None):
        self.set_port(self.PROTO_TCP, source, target)

    def unset_port(self, protocol, source):
        self._raise_for_protocol(protocol)

        if not self.has_port(protocol, source):
            raise ValueError("Invalid port: {}".format(str(source)))

        del self[protocol][int(source)]

    def unset_tcp_port(self, source):
        self.unset_port(self.PROTO_TCP, source)

    def list_ports(self, protocol):
        self._raise_for_protocol(protocol)

        return self[protocol].keys()

    def list_tcp_ports(self):
        return self.list_ports(self.PROTO_TCP)

    def has_port(self, protocol, source):
        self._raise_for_protocol(protocol)

        if int(source) not in self.list_ports(protocol):
            return False

        return True

    def has_tcp_port(self, source):
        return self.has_port(self.PROTO_TCP, source)

    def get_port(self, protocol, source):
        if not self.has_port(protocol, source):
            raise ValueError("Port {} is not mapped".format(str(source)))

        return self[protocol][int(source)]

    def get_tcp_port(self, source):
        return self.get_port(self.PROTO_TCP, source)

    def get_protocols(self):
        return self.keys()


class PortMapCollisionException(Exception):
    pass


class PortMap(PortList):
    def set_port(self, protocol, source, target=None):
        self._raise_for_protocol(protocol)

        if not target:
            target = source
        elif isinstance(target, list):
            for port in target:
                self.set_port(protocol, source, port)
            return

        source = int(source)
        target = int(target)

        # Check if there isn't map colision on right side
        for used_source, used_tport_set in self[protocol].items():
            if used_source != source and target in used_tport_set:
                raise PortMapCollisionException("Target port {} has been already mapped".format(target))

        if not self.has_port(protocol, source):
            data = []
        else:
            data = self.get_port(protocol, source)
            if target in data:
                return

        data.append(target)

        super(PortMap, self).set_port(protocol, source, data)
