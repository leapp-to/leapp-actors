from jsl import Document
from jsl.fields import DictField, StringField, DocumentField


# PORT_PATTERN =     1 -  9999
#                10000 - 59999
#                60000 - 64000
#                65000 . 65499
#                65500 - 65529
#                65530 - 65535

PORT_PATTERN = "^[1-9][0-9]{0,3}$|" \
               "^[1-5][0-9]{4}$|" \
               "^6[0-4][0-9]{3}$|" \
               "^65[0-4][0-9]{2}$|" \
               "^655[0-2][0-9]$|" \
               "^6553[0-5]$"


class PortData(Document):
    name = StringField(required=True)
    product = StringField()


class TypePortScan(Document):
    tcp = DictField(pattern_properties={PORT_PATTERN: DocumentField(PortData, as_ref=True)},
                    additional_properties=False)
    udp = DictField(pattern_properties={PORT_PATTERN: DocumentField(PortData, as_ref=True)},
                    additional_properties=False)
