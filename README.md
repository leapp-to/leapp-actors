# Actor Definitions

There are two kinds of definitions:

1. Actor Definition
2. Actor Extension Definition

Extension definitions allow to specialize other actor definitions
and build new actors trough this. Extensions also allow for connecting
two unrelated previously unrelated names.

## Actor Definition Format

```yaml
---
inputs:
  - name: input_channel_name
    type:
      name: schema_name_reference
outputs:
  name: output_channel_name
  type:
    name: schema_name_reference
description: |
  Text field to describe what this actor is doing and a potential place
  for documenting the inputs and outputs
executor:
    type: registered-name-of-executor
    ... executor specific fields
```

## Actor Extension Definition Format

```yaml
---
inputs:
  - name: input_channel_name
    type:
      name: schema_name_reference
outputs:
  name: output_channel_name
  type:
    name: schema_name_reference
description: |
  Text field to describe what this actor is doing and a potential place
  for documenting the inputs and outputs
extends:
  name: actor_name_to_extend
  inputs:
    - name: input_channel_name_of_the_extended_actor
      value: value_to_pass
    - name: input_channel_name_of_the_extended_actor2
      source: '@input_channel_name.to.pass.through.to.the.actor.in.reference.notation@'
  outputs:
    - name: output_channel_name
      source: '@output_channel_name.to.return.in.reference.notation@'

```

# Actor executors

Visit: https://github.com/leapp-to/snactor#user-content-provided-executors

