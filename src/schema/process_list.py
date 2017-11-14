import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class ProcessList(jsl.Document):
    processes = jsl.ArrayField(jsl.DictField())
