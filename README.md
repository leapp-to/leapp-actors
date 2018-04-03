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


---


# How to write actor tests

Here are some key points to read before you start to write tests:


## Actor dependencies

Each actor can now have its own Makefile with `install-deps` target. This takes care of installing any dependencies of your actor.
So, if your actor has any dependency, put it there.

See augeas example here: https://github.com/leapp-to/leapp-actors/blob/master/src/actors/common/augeas/Makefile


## Naming conventions

Put tests inside `tests` directory in your actor directory.

Tests should adhere to the following naming convention:
- **You have to name your test scripts/files/functions/methods/whatever with the "test_" prefix.
e.g. for augeas: tests/test_augeas.py which contains test_augeas() function.**

Testing framework (pytest) is collecting tests based on this particular naming, so if you name your test file `check_my_actor.py`, your test will not be collected.
Also, if you have file `test_augeas.py` with `check_augeas()` test function, your test will not be collected.

Example here: https://github.com/leapp-to/leapp-actors/tree/master/src/actors/common/augeas


## Running actors from the test code

`tests/test_schema.py` is always running first, which ensures that actors/schemas are registered.
Test writer should not care about this, this is done by the framework.
Therefore, do not load actors/schemas from your test code (you will get `actor already registered/loaded` exception when you do).
All you need to do in your test code is to use `snactor.loader`, get the actor and execute.

See example here: https://github.com/leapp-to/leapp-actors/blob/master/src/actors/common/augeas/tests/test_augeas.py

In the future, we are planning to implement some set of helper/utility functions that should make testing easier (e.g. comparing expected vs actual actor outputs).


## Running tests locally

If you want to run all tests from leapp-actors, run the following from the leapp-actors directory:

``` bash
$ make test
```

You can also do:

``` bash
$ make test ACTOR=augeas
```

which runs all test files with the `augeas` substring in the name. This is nice if you want to run only tests from one specific actor.

It is also possible to generate junit-like xml report and save it into file:

``` bash
$ make test REPORT=report.xml
```
