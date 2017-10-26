import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class IPList(jsl.Document):
    ips = jsl.ArrayField(jsl.IPv4Field())
