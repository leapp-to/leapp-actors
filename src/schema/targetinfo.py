import jsl


class TargetInfo(jsl.Document):
    docker = jsl.ArrayField(jsl.StringField(), max_items=2)
    rsync = jsl.ArrayField(jsl.StringField(), max_items=2)
    containers = jsl.ArrayField([
        jsl.StringField(),
        jsl.ArrayField(jsl.StringField())
    ])
