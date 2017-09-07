from jsl import Document
from jsl.fields import ArrayField, StringField


class TypeStringList(Document):
    value = ArrayField(items=StringField(), unique_items=True, additional_items=False)
