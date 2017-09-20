import jsl


class AnsibleSetupModuleFacts(jsl.Document):
    class Options(object):
        additional_properties = True
    ansible_facts = jsl.DictField(required=False)
