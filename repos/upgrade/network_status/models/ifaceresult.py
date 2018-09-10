from leapp.models import Model, fields
from leapp.topics import NetworkInfoTopic


class IfacesInfo(Model):
    topic = NetworkInfoTopic
    if_name = fields.String(required=True)
    hwaddr = fields.String(required=True)
    driver = fields.String(required=True)
    ipv4addr = fields.String(required=True)


class IfaceResult(Model):
    topic = NetworkInfoTopic
    items = fields.List(fields.Nested(IfacesInfo), required=True, default=[])
