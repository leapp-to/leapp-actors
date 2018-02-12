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

install:
	mkdir -p $(ROOT_PATH)
	cp -r src/actors $(ROOT_PATH)
	cp -r src/schemas $(ROOT_PATH)

test:
	py.test

.PHONY: clean install test install-deps build
