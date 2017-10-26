import jsl
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class AnsibleSetupModuleFacts(jsl.Document):
    class Options(object):
        additional_properties = True
    ansible_facts = jsl.DictField(required=False)
