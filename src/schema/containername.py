from jsl import Document
from jsl.fields import StringField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class ContainerName(Document):
    value = StringField(pattern='^[a-zA-Z0-9][a-zA-Z0-9_.-]+$', required=True,
                        description='Valid container name. Same pattern used by Docker.')


@registered_schema('1.0')
class OptionalContainerName(Document):
    value = StringField(pattern='^([a-zA-Z0-9][a-zA-Z0-9_.-]+|)$', required=False,
                        description='Valid container name. Same pattern used by Docker.')
