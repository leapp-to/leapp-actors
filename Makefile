ROOT_PATH=$(PREFIX)/usr/share/leapp

clean:
	@rm -rf build/ dist/ *.egg-info
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

build:
	true

# dependencies for the new framework
install-deps-new:
	virtualenv -p /usr/bin/python2.7 tut; \
	. tut/bin/activate; \
	pip install --upgrade setuptools; \
	pip install -r requirements_new.txt

# runs tests using new framework
test-new:
	. tut/bin/activate; \
	python utils/run_new_pytest.py --actor=$(ACTOR) --report=$(REPORT)

.PHONY: clean test-new install-deps-new build
