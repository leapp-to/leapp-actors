import jsl
from leapp.core import Endpoint, OwnedObject, ABSOLUTE_PATH_PATTERN


class DatabaseConnection(jsl.Document):
    class Options(object):
        definition_id = 'database_settings'

    database = jsl.StringField()
    username = jsl.StringField()
    password = jsl.StringField()


class DatabaseMigration(jsl.Document):
    class Options(object):
        definition_id = 'database_migration'

    backend = jsl.StringField(enum=['postgresql', 'mysql'])
    connection = jsl.DocumentField(DatabaseConnection)
    endpoint = jsl.DocumentField(Endpoint)


class DjangoMigration(OwnedObject):
    class Options(object):
        definition_id = 'django_migration'

    database = jsl.DocumentField(DatabaseMigration)
    cache = jsl.DocumentField(Endpoint)
    config_files = jsl.ArrayField(jsl.StringField(pattern=ABSOLUTE_PATH_PATTERN))
    app_root = jsl.StringField(pattern=ABSOLUTE_PATH_PATTERN)
