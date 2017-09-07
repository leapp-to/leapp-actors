import jsl


class OSVersion(jsl.Document):
    name = jsl.StringField()
    version = jsl.StringField()
