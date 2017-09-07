import jsl


class RPMPackage(jsl.Document):
    name = jsl.StringField()
    version = jsl.StringField()


class RPMPackages(jsl.Document):
    packages = jsl.ArrayField(jsl.DocumentField(RPMPackage()))
