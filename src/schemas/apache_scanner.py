import jsl
from snactor.registry.schemas import registered_schema

@registered_schema('1.0')
class ApacheScanner(jsl.Document):
    class Options(object):
        definition_id = 'ApacheScanner'

    IncludeOptional = jsl.ArrayField(jsl.StringField(required=True), required=False)
    User = jsl.ArrayField(jsl.StringField(required=True), required=False)
    Group = jsl.ArrayField(jsl.StringField(required=True), required=False)
    Mutex = jsl.ArrayField(jsl.StringField(required=True), required=False)
    PidFile = jsl.ArrayField(jsl.StringField(required=True), required=False)
    Listen = jsl.ArrayField(jsl.StringField(required=True), required=False)
    TypesConfig = jsl.ArrayField(jsl.StringField(required=True), required=False)
    CacheRoot = jsl.ArrayField(jsl.StringField(required=True), required=False)
    MIMEMagicFile = jsl.ArrayField(jsl.StringField(required=True), required=False)
    ScriptSock = jsl.ArrayField(jsl.StringField(required=True), required=False)
    SSLCertificateKeyFile = jsl.ArrayField(jsl.StringField(required=True), required=False)
    SSLCertificateFile = jsl.ArrayField(jsl.StringField(required=True), required=False)
    CustomLog = jsl.ArrayField(jsl.StringField(required=True), required=False)
    ErrorLog = jsl.ArrayField(jsl.StringField(required=True), required=False)
    Include = jsl.ArrayField(jsl.StringField(required=True), required=False)
    VirtualHost = jsl.ArrayField(jsl.StringField(required=True), required=False)
    Directory = jsl.ArrayField(jsl.StringField(required=True), required=False)
    DocumentRoot = jsl.ArrayField(jsl.StringField(required=True), required=False)
    absolute_path = jsl.ArrayField(jsl.StringField(required=True), required=False)
    LoadModule = jsl.ArrayField(jsl.StringField(required=True), required=False)
