import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class PortMapping(jsl.Document):
    protocol = jsl.StringField(enum=['udp', 'tcp'], required=True)
    exposed_port = jsl.IntField(minimum=1, maximum=65535, required=False)
    port = jsl.IntField(minimum=1, maximum=65535, required=True)


@registered_schema('1.0')
class ExposedPorts(jsl.Document):
    ports = jsl.ArrayField(jsl.DocumentField(PortMapping, as_ref=True), required=True)
