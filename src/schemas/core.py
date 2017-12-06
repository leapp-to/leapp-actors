''' Leapp core data schemas  '''

import jsl


# Absolute path, excluding `/` root directory because both Docker^WMoby and OpenShift do not
# allow overriding `/`
ABSOLUTE_PATH_PATTERN = r'^/\w{1,}'


class LeappSchemaBase(jsl.Document):
    class Options(object):
        definition_id = 'leapp_base_schema'

    ''' Id of our current document '''
    _id = jsl.StringField(required=True)

    ''' Id of an document that pre-dates this one '''
    _rid = jsl.StringField()


class Credentials(LeappSchemaBase):
    class Options(object):
        definition_id = 'credentials'

    user_name = jsl.StringField(required=True)
    password = jsl.StringField(required=True)


class Host(LeappSchemaBase):
    class Options(object):
        definition_id = 'host'

    hostname = jsl.StringField()
    ip_addresses = jsl.ArrayField(jsl.IPv4Field)  # TODO: IPv6
    alias = jsl.StringField()


class OwnedObject(LeappSchemaBase):
    ''' Base schema class for any objects that are owned by some higher-level construct or constructs
        - this effectively allows us to organize things in a graph (if we treat owner as parent)

        If the above abstract mumbo-jumbo doesn't ring a bell for you let me shed some more
        practical light as to why this is a good idea:

        * Owner should be an app, aka the thing being containerized, so if I, for example, add
          a file system fragment owned by [app, apache] what I'm really trying to express is that
          the given fragment should be part of the resulting Apache container

        * Owner also can be something completely different, and the relationship betweem the owner
          and the owned object fully depends on the characteristics of the contract between the actor
          that created an "owner" and an actor that created a resource owned by the "owner"

        * Think of this as an "foreign key" in a relational database that allows us unidirectionaly
          link two data objects together
    '''
    owners = jsl.ArrayField(jsl.StringField())


class BuildSpec(jsl.Document):
    class Options(object):
        definition_id = 'build_spec'

    base_image = jsl.StringField()
    build_type = jsl.StringField(enum=['s2i', 'container'])


class AppDefinition(jsl.Document):
    class Options(object):
        definition_id = 'app_definition'

    # Packages / Image, Either / Or
    packages = jsl.ArrayField(jsl.StringField())
    image = jsl.StringField()
    build = jsl.DocumentField(BuildSpec)

    name = jsl.StringField()


class FSFragment(OwnedObject):
    class Options(object):
        definition_id = 'filesystem_fragment'

    source = jsl.DocumentField(Host, required=True)
    path = jsl.StringField(pattern=ABSOLUTE_PATH_PATTERN, required=True)
    kind = jsl.StringField(enum=['file', 'directory'], required=True)
    # if the fragment is static it will be baked into the image
    # otherwise the fragment will be put onto a persistent storage and bind mounted
    # into the container
    static = jsl.BooleanField()
    target_path = jsl.StringField(pattern=ABSOLUTE_PATH_PATTERN, required=True)


class SynthesizedFile(OwnedObject):
    class Options(object):
        definition_id = 'synthesized_file'

    path = jsl.StringField(pattern=ABSOLUTE_PATH_PATTERN, required=True)
    contents = jsl.StringField()


class PatchedFile(OwnedObject):
    class Options(object):
        definition_id = 'pacthed_file'

    # TODO: validate that file.kind == 'file'
    file = jsl.DocumentField(FSFragment)
    patch = jsl.StringField()


class Endpoint(OwnedObject):
    class Options(object):
        definition_id = 'endpoint'

    # TODO: Maybe do jsl.OneOf(jsl.IPv4Field, jsl.StringField) ?>??
    address = jsl.StringField()
    port = jsl.IntField(minimum=1, maximum=65535)


class NetworkService(OwnedObject):
    class Options(object):
        definition_id = 'network_service'

    source = jsl.DocumentField(Host)
    endpoint = jsl.DocumentField(Endpoint)


class Diagnostics(jsl.Document):
    class Options(object):
        definition_id = 'diagnostics'

    severity = jsl.StringField(enum=['log', 'debug', 'fatal'], required=True)
    message = jsl.StringField(required=True)
    data = jsl.DictField()
