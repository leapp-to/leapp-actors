from jsl import Document
from jsl.fields import BooleanField, StringField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class TypePortScanOptions(Document):
    shallow_scan = BooleanField(required=False)
    port_range = StringField(required=False)
    force_nmap = BooleanField(required=False)
