import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class DockerInfo(jsl.Document):
    path = jsl.ArrayField([
        jsl.IntField(),
        jsl.StringField()
    ])
    systemd_state = jsl.ArrayField([
        jsl.IntField(),
        jsl.StringField()
    ])
    info = jsl.ArrayField([
        jsl.IntField(),
        jsl.StringField()
    ])
