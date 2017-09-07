import jsl


class RSyncInfo(jsl.Document):
    path = jsl.ArrayField([
        jsl.IntField(),
        jsl.StringField()
    ])
    version = jsl.ArrayField([
        jsl.IntField(),
        jsl.StringField()
    ])
