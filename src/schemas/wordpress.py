import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class Version(jsl.Document):
    value = jsl.StringField(required=True)


@registered_schema('1.0')
class DatabaseHost(jsl.Document):
    value = jsl.IPv4Field(required=True)


@registered_schema('1.0')
class RootDirectory(jsl.Document):
    value = jsl.StringField(required=True)
