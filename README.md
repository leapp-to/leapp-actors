# Tutorial
Checkout the tutorial for [creating first actor](https://leapp.readthedocs.io/en/latest/first-actor.html)

---

# How to write actor tests

Here are some key points to read before you start to write tests:

## Actor dependencies

Each actor can now have its own Makefile with `install-deps` target. This
takes care of installing any dependencies of your actor. So, if your actor has
any dependency, put it there.

See testing actor's examle [here](repos/common/actors/testactor/Makefile).

To install dependencies for all actors, run:

``` bash
$ make install-deps
```

Or for just one specific actor:

``` bash
$ make install-deps ACTOR=testactor
```

## Naming conventions

Put tests inside `tests` directory in your actor directory, as stated in the
[directory layout](https://leapp.readthedocs.io/en/latest/best-practises.html#repository-directory-layout).

In order to have the tests discovered and carried out by
[pytest framework](https://pytest.org), you have to follow these rules:
- All tests has to reside in `test_*.py` or `*_test.py` files
- Test functions outside of class has to be `test_` prefixed
- Test methods with `test_` prefix has to reside in `Test` prefixed classes

More on that in [pytest documentation](https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery).

## Running tests locally

If you want to run all tests from leapp-actors, run the following code from
leapp-actors directory:

``` bash
$ make test
```

You can also do:

``` bash
$ make test ACTOR=testactor
```

which runs all test files with the `testactor` substring in the name. This is
useful if you want to test only one specific actor.

It is also possible to generate report in JUnit XML format:

``` bash
$ make test REPORT=report.xml
```
