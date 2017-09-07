import jsl


class ContainersList(jsl.Document):
    retcode = jsl.IntField()
    containers = jsl.ArrayField(jsl.StringField())
