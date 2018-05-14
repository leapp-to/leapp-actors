# Tutorial
Checkout the [leapp actor tutorials](https://leapp.readthedocs.io/en/latest/tutorials.html)


---


# How to write actor tests

Here are some key points to read before you start to write tests:


## Actor dependencies

Each actor can now have its own Makefile with `install-deps` target. This takes care of installing any dependencies of your actor.
So, if your actor has any dependency, put it there.

See augeas example here: https://github.com/leapp-to/leapp-actors/blob/master/src/actors/common/augeas/Makefile


## Naming conventions

Put tests inside `tests` directory in your actor directory, as stated in the
[directory layout](https://leapp.readthedocs.io/en/latest/best-practises.html#repository-directory-layout).

In order to have the tests discovered bnd carried out by
[pytest framework](https://pytest.org), you have to follow these rules:
- All tests has to reside in `test_*.py` or `*_test.py` files
- Test functions outside of class has to be `test_` prefixed
- Test methods with `test_` prefix has to reside in `Test` prefixed classes

More on that in [pytest documentation](https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery).

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
