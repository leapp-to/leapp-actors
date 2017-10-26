from jsl import Document
from jsl.fields import NumberField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class BaseTypeNumber(Document):
    value = NumberField()
