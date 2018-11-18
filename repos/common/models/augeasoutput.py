from leapp.models import Model, fields
from leapp.topics import SystemInfoTopic


# TODO: help text for fields

class AugeasLensItem(Model):
    topic = SystemInfoTopic

    name = fields.String(required=True)
    absolute_path = fields.String(required=True)
    properties = fields.String(required=True)


class AugeasLensesList(Model):
    topic = SystemInfoTopic

    lens_name = fields.String(required=True)
    lens_items = fields.List(fields.Model(AugeasLensItem))


class AugeasOutput(Model):
    topic = SystemInfoTopic

    items = fields.List(fields.Model(AugeasLensesList), default=[])
