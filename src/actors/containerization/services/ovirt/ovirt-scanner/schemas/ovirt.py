import jsl
from snactor.registry.schemas import registered_schema


class OVirtRPM(jsl.DocumentField):
    name = jsl.StringField(required=True)
    version = jsl.StringField(required=True)


class OVirtServiceField(jsl.DocumentField):
    service = jsl.StringField(required=True)
    rpm = jsl.DocumentField(OVirtRPM, required=True)


@registered_schema('1.0')
class OVirtScanResult(jsl.DocumentField):
    class Options(object):
        definition_id = 'OVirtScanResult'
    engine = jsl.BooleanField(required=True)
    dwh = jsl.BooleanField(required=True)
    imageio = jsl.BooleanField(required=True)
    websocket = jsl.BooleanField(required=True)
    vmconsole = jsl.BooleanField(required=True)
    services = jsl.ArrayField(jsl.DocumentField(OVirtServiceField), required=True)

