from jsl import Document
from jsl.fields import BooleanField, StringField


class TypePortScanOptions(Document):
    shallow_scan = BooleanField(required=False)
    port_range = StringField(required=False)
    force_nmap = BooleanField(required=False)
