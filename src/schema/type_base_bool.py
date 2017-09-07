from jsl import Document
from jsl.fields import BooleanField


class BaseTypeBool(Document):
    value = BooleanField()
