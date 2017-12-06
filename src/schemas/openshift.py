import jsl

from leapp.core import ABSOLUTE_PATH_PATTERN


TOKEN_PATTERN = r'^[a-fA-F0-9]*'


class OpenshiftLogin(jsl.Document):
    class Options(object):
        definition_id = 'openshift_login'

    token = jsl.StringField(pattern=TOKEN_PATTERN, required=True)


class OpenshiftBuildSpec(jsl.Document):
    class Options(object):
        definition_id = 'openshift_build_spec'

    strategy = jsl.StringField(enum=['docker', 's2i'], required=True)
    base = jsl.StringField(required=True)
    target = jsl.StringField(required=True)
    arguments = jsl.ArrayField(jsl.StringField(), required=True)
    source_directory = jsl.StringField(pattern=ABSOLUTE_PATH_PATTERN)


class OpenshiftLivePod(jsl.Document):
    class Options(object):
        definition_id = 'openshift_live_pod'

    name = jsl.StringField(required=True)
    spec = jsl.StringField(required=True)


class OpenshiftLiveBuild(OpenshiftLivePod):
    class Options(object):
        definition_id = 'openshift_live_build'

    build_spec = jsl.DocumentField(OpenshiftBuildSpec, required=True, as_ref=True)
