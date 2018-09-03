from jsl import Document
from jsl.fields import ArrayField, BooleanField, DictField, DocumentField, StringField
from snactor.registry.schemas import registered_schema


class ConfigFile(Document):
    path = StringField(required=True)
    properties = ArrayField(items=DictField(), additional_items=False)


class PostgreSQLInstance(Document):
    postgresql_conf = DocumentField(ConfigFile())
    pg_hba_conf = DocumentField(ConfigFile())


@registered_schema('1.0')
class TypePostgreSQLDetectionResult(Document):
    instances = ArrayField(items=DocumentField(PostgreSQLInstance()))
