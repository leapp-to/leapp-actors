import jsl


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
