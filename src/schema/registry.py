import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class RegistryEntry(jsl.Document):
    address = jsl.StringField(required=True)
    user = jsl.StringField(required=True)
    password = jsl.StringField(required=True)


@registered_schema('1.0')
class ContainerRegistry(jsl.Document):
    value = jsl.DocumentField(RegistryEntry())
