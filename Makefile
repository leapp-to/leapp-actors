ROOT_PATH=$(PREFIX)/usr/share/leapp

SNACTOR_URL=https://github.com/leapp-to/snactor.git
SNACTOR_BRANCH=master

clean:
	@rm -rf build/ dist/ *.egg-info
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

build:
	true

install-deps:
	pip install -r requirements.txt
	rm -rf snactor
	git clone $(SNACTOR_URL) snactor
	cd snactor && git checkout $(SNACTOR_BRANCH) && make install-deps build install
	rm -fr snactor
	python utils/install_actor_deps.py --actor=$(ACTOR)

install:
	mkdir -p $(ROOT_PATH)
	cp -r src/actors $(ROOT_PATH)
	cp -r src/schemas $(ROOT_PATH)

test:
	python utils/run_pytest.py --actor=$(ACTOR) --report=$(REPORT)

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


.PHONY: clean install test test-new install-deps install-deps-new build
