import jsl

class Service(jsl.Document):
    class Options(object):
        definition_id = 'service'

    exe = jsl.StringField()
    command_line = jsl.StringField()
    env = jsl.DictField()


class Services(jsl.Document):
    class Options(object):
        definition_id = 'services'

    services = jsl.ArrayField(jsl.DocumentField(Service))