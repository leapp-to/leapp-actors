ROOT_PATH=$(PREFIX)/usr/share/leapp

clean:
	@rm -rf build/ dist/ *.egg-info
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

build:
	true

install-deps:
	virtualenv -p /usr/bin/python2.7 tut; \
	. tut/bin/activate; \
	pip install --upgrade setuptools; \
	pip install -r requirements.txt

test:
	. tut/bin/activate; \
	python utils/run_pytest.py --actor=$(ACTOR) --report=$(REPORT)

.PHONY: clean test install-deps build
