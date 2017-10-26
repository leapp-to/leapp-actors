from jsl import Document
from jsl.fields import BooleanField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class BaseTypeBool(Document):
    value = BooleanField()
