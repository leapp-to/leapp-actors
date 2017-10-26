import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class RPMPackage(jsl.Document):
    name = jsl.StringField()
    version = jsl.StringField()


@registered_schema('1.0')
class RPMPackages(jsl.Document):
    packages = jsl.ArrayField(jsl.DocumentField(RPMPackage()))
