from jsl import Document
from jsl.fields import ArrayField, StringField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class StringList(Document):
    value = ArrayField(items=StringField(), additional_items=False)
