from jsl import Document
from jsl.fields import NumberField


class BaseTypeNumber(Document):
    value = NumberField()
