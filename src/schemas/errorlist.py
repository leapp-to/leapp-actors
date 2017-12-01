from jsl import Document, DocumentField
from jsl.fields import ArrayField, StringField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class Error(Document):
    context = StringField()
    value = StringField()


@registered_schema('1.0')
class ErrorList(Document):
    value = ArrayField(items=DocumentField(Error, as_ref=True), additional_items=False)
