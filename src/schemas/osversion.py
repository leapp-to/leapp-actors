import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class OSVersion(jsl.Document):
    name = jsl.StringField()
    version = jsl.StringField()
