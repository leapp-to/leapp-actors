from jsl import Document
from jsl.fields import StringField


class Message(Document):
    value = StringField()
