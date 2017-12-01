from jsl import Document
from jsl.fields import StringField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class String(Document):
    value = StringField()
