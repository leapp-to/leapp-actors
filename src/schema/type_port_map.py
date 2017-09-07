from jsl import Document
from jsl.fields import DictField, IntField, ArrayField


SOURCE_PORT_PATTERN = "^[1-9][0-9]{0,3}$|" \
                      "^[1-5][0-9]{4}$|" \
                      "^6[0-4][0-9]{3}$|" \
                      "^65[0-4][0-9]{2}$|" \
                      "^655[0-2][0-9]$|" \
                      "^6553[0-5]$"


class PortField(IntField):
    def __init__(self):
        super(PortField, self).__init__(minimum=1,
                                        maximum=65535,
                                        exclusive_minimum=True,
                                        exlusive_maximum=True)


class TargetPortListField(ArrayField):
    def __init__(self):
        super(TargetPortListField, self).__init__(items=PortField(),
                                                  min_items=1,
                                                  unique_items=True,
                                                  additional_items=False)


class TypePortMap(Document):
    tcp = DictField(pattern_properties={SOURCE_PORT_PATTERN: TargetPortListField()},
                    additional_properties=False)
    udp = DictField(pattern_properties={SOURCE_PORT_PATTERN: TargetPortListField()},
                    additional_properties=False)
