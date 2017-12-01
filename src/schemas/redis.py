import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class RedisEntry(jsl.Document):
    version = jsl.StringField(required=True)
    config_file_path = jsl.StringField()
    db_file_path = jsl.StringField()


@registered_schema('1.0')
class RedisInstallation(jsl.Document):
    value = jsl.DocumentField(RedisEntry())
