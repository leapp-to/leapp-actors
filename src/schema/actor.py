import jsl


class ChannelSpec(jsl.Document):
    name = jsl.StringField(required=True)
    type = jsl.StringField(required=True)


class ExtendsChannelValue(jsl.Document):
    name = jsl.StringField(required=True)
    value = jsl.StringField(required=True)


class ExtendsChannelInputRef(jsl.Document):
    name = jsl.StringField(required=True)
    source = jsl.StringField(required=True)


class ExtendsChannelOutputRef(jsl.Document):
    name = jsl.StringField(required=True)
    target = jsl.StringField(required=True)


class ExtendsDefinition(jsl.Document):
    inputs = jsl.ArrayField(jsl.OneOfField([
        jsl.DocumentField(ExtendsChannelValue, as_ref=True),
        jsl.DocumentField(ExtendsChannelInputRef, as_ref=True)
    ]))
    outputs = jsl.ArrayField(jsl.OneOfField([
        jsl.DocumentField(ExtendsChannelValue, as_ref=True),
        jsl.DocumentField(ExtendsChannelOutputRef, as_ref=True)
    ]))
    name = jsl.StringField(required=True)


class ActorDefinition(jsl.Document):
    inputs = jsl.ArrayField(jsl.DocumentField(ChannelSpec, as_ref=True))
    output = jsl.OneOfField([
        jsl.DocumentField(ChannelSpec, as_ref=True),
        jsl.ArrayField(jsl.DocumentField(ChannelSpec, as_ref=True))])
    description = jsl.StringField()
    extends = jsl.DocumentField(ExtendsDefinition, as_ref=True)
    executor = None  # This needs to be defined on runtime and needs to be a jsl.OneOfField
