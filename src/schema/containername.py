from jsl import Document
from jsl.fields import StringField


class ContainerName(Document):
    value = StringField(pattern='^[a-zA-Z0-9][a-zA-Z0-9_.-]+$', required=True,
                        description='Valid container name. Same pattern used by Docker.')


class OptionalContainerName(Document):
    value = StringField(pattern='^([a-zA-Z0-9][a-zA-Z0-9_.-]+|)$', required=False,
                        description='Valid container name. Same pattern used by Docker.')
