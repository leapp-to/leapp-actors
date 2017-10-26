import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class TargetInfo(jsl.Document):
    docker = jsl.ArrayField([
        jsl.StringField(),
        jsl.OneOfField([jsl.StringField(), jsl.NullField()])
    ])
    rsync = jsl.ArrayField([
        jsl.StringField(),
        jsl.OneOfField([jsl.StringField(), jsl.NullField()])
    ])
    containers = jsl.ArrayField([
        jsl.StringField(),
        jsl.ArrayField(jsl.StringField())
    ])
