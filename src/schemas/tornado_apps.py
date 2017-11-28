import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class TornadoApps(jsl.Document):
    apps = jsl.ArrayField(jsl.DictField())
