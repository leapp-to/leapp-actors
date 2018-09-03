from jsl import Document
from jsl.fields import ArrayField, BooleanField, StringField

from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class AppSatelliteDetectionResult(Document):
    satellite_detected = BooleanField(default=False, required=True)
    satellite_version_major = StringField(default=None, required=False)
    satellite_version_minor = StringField(defauult=None, required=False)
    satellite_version_bugfix = StringField(default=None, required=False)
    satellite_services = ArrayField(items=StringField(), unique_items=True, min_items=0, required=False)
