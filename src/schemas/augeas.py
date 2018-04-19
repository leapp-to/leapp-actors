import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class AugeasLensProperties(jsl.Document):
    class Options(object):
        definition_id = 'AugeasLensProperties'
    name = jsl.StringField(required=True)
    value = jsl.OneOfField([jsl.StringField(), jsl.NullField()])
    properties = jsl.ArrayField(jsl.DocumentField(jsl.RECURSIVE_REFERENCE_CONSTANT))


@registered_schema('1.0')
class AugeasLensResult(jsl.Document):
    class Options(object):
        definition_id = 'AugeasLensResult'
    name = jsl.StringField(required=True)
    absolute_path = jsl.StringField(required=True)
    properties = jsl.ArrayField(jsl.DocumentField(AugeasLensProperties))

@registered_schema('1.0')
class AugeasInput(jsl.Document):
    class Options(object):
        definition_id = 'AugeasInput'
    load_files = jsl.ArrayField(jsl.StringField(required=False), required=False)
    directives = jsl.ArrayField(jsl.StringField(required=False), required=False)
    lens = jsl.StringField(required=False)
    prefix_for_relative = jsl.StringField(required=False)
