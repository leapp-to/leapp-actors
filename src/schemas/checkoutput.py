from jsl import Document, DocumentField
from jsl.fields import ArrayField, StringField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class CheckEntry(Document):
    check_actor = StringField(required=True)
    check_action = StringField()
    status = StringField(required=True, enum=['PASS', 'FAIL'])
    summary = StringField(required=True)
    params = ArrayField(items=StringField(), unique_items=True, additional_items=False)


@registered_schema('1.0')
class CheckOutput(Document):
    checks = ArrayField(items=DocumentField(CheckEntry, as_ref=True), additional_items=False)
