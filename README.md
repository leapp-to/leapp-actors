# How to write actors

See the tutorial for [creating the first actor](https://leapp.readthedocs.io/en/latest/first-actor.html).

---

# How to write actor tests

Please read documentation about [how to unit test actors](https://leapp.readthedocs.io/en/latest/unit-testing.html).

## Actor dependencies

Each actor can now have its own Makefile with the `install-deps` target. This
takes care of installing any dependencies of your actor. If your actor has
any dependencies, include them in the Makefile.

See the testing actor's example [here](repos/common/actors/testactor/Makefile).

To install dependencies for all actors, run:

``` bash
$ make install-deps
```

For just one specific actor, run:

``` bash
$ make install-deps ACTOR=testactor
```

## Running tests locally

To run all tests from leapp-actors, run the following code from
the `leapp-actors` directory:

``` bash
$ make test
```

It is also possible to generate a report in a JUnit XML format:

``` bash
$ make test REPORT=report.xml
```
