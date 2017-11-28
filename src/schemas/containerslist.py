import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class ContainersList(jsl.Document):
    retcode = jsl.IntField()
    containers = jsl.ArrayField(jsl.StringField())
