import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class RSyncInfo(jsl.Document):
    path = jsl.ArrayField([
        jsl.IntField(),
        jsl.StringField()
    ])
    version = jsl.ArrayField([
        jsl.IntField(),
        jsl.StringField()
    ])
