import jsl


class AugeasLensProperties(jsl.Document):
    class Options(object):
        definition_id = 'AugeasLensProperties'
    name = jsl.StringField(required=True)
    value = jsl.OneOfField([jsl.StringField(), jsl.NullField()])
    properties = jsl.ArrayField(jsl.DocumentField(jsl.RECURSIVE_REFERENCE_CONSTANT))


class AugeasLensResult(jsl.Document):
    class Options(object):
        definition_id = 'AugeasLensResult'
    name = jsl.StringField(required=True)
    absolute_path = jsl.StringField(required=True)
    properties = jsl.ArrayField(jsl.DocumentField(AugeasLensProperties))
