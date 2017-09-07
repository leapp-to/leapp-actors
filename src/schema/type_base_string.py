from jsl import Document
from jsl.fields import StringField


class BaseTypeString(Document):
    value = StringField()
