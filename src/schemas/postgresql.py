import jsl
from leapp.core import ABSOLUTE_PATH_PATTERN, Credentials, LeappSchemaBase


class PostgresqlUser(LeappSchemaBase):
    class Options(object):
        definition_id = 'postgresql_user'

    credentials = jsl.DocumentField(Credentials)
    database_name = jsl.StringField(rquired=True)


class RawPostgresqlDatabase(jsl.Document):
    class Options(object):
        definition_id = 'postgresql_database'

    system_user_id = jsl.StringField(default='postgres')
    user = jsl.DocumentField(PostgresqlUser)
    config_path = jsl.StringField(pattern=ABSOLUTE_PATH_PATTERN, required=True)


class PostgresqlDatabase(jsl.Document):
    class Options(object):
        definition_id = 'postgresql_database'

    system_user_id = jsl.StringField(default='postgres')
    credentials = jsl.ArrayField(jsl.DocumentField(Credentials))


class PostgresqlSnapshot(LeappSchemaBase):
    class Options(object):
        definition_id = 'postgresql_snapshot'

    payload = jsl.StringField(required=True)
