import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class OVirtContainerError(jsl.DocumentField):
    class Options(object):
        definition_id = 'OVirtContainerError'
    message = jsl.StringField()


@registered_schema('1.0')
class OVirtContainer(jsl.DocumentField):
    class Options(object):
        definition_id = 'OVirtContainer'
    container_name = jsl.StringField(required=True)
    container_id = jsl.StringField(required=False)
    errors = jsl.ArrayField(OVirtContainerError, required=False)
