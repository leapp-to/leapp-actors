import jsl


class PortMapping(jsl.Document):
    protocol = jsl.StringField(enum=['udp', 'tcp'], required=True)
    exposed_port = jsl.IntField(minimum=1, maximum=65535, required=False)
    port = jsl.IntField(minimum=1, maximum=65535, required=True)


class ExposedPorts(jsl.Document):
    ports = jsl.ArrayField(jsl.DocumentField(PortMapping, as_ref=True), required=True)
