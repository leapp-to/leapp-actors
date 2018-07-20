# How to write actors

See the tutorial for [creating the first actor](https://leapp.readthedocs.io/en/latest/first-actor.html).

---

# How to write actor tests

Please read documentation about [how to unit test actors](https://leapp.readthedocs.io/en/latest/unit-testing.html).

## Actor dependencies

Each actor can now have its own Makefile with the `install-deps` target. This
takes care of installing any dependencies of your actor. If your actor has
any dependencies, put them there.

See the testing actor's example [here](repos/common/actors/testactor/Makefile).

To install dependencies for all actors, run:

``` bash
$ make install-deps
```

Or, for just one specific actor, run:

``` bash
$ make install-deps ACTOR=testactor
```

## Naming conventions

Put tests inside the `tests` directory in your actor directory, as stated in the
[directory layout](https://leapp.readthedocs.io/en/latest/best-practises.html#repository-directory-layout).

In order to have the tests found and carried out by
[pytest framework](https://pytest.org), follow these rules:
- All tests have to reside in the `test_*.py` or `*_test.py` files.
- Test functions outside of the class have to be  prefixed by `test_`.
- Test methods with the `test_` prefix have to reside in the `Test` prefixed classes.

More on that in the [pytest documentation](https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery).

## Running tests locally

If you want to run all tests from leapp-actors, run the following code from
the leapp-actors directory:

``` bash
$ make test
```

You can also use:

``` bash
$ make test ACTOR=testactor
```

which runs all test files with the `testactor` substring in the name. This is
useful if you want to test only one specific actor.

It is also possible to generate a report in a JUnit XML format:

``` bash
$ make test REPORT=report.xml
```
