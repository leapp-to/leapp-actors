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
ifeq ($(ACTOR), )
	for i in $$(find src -type f -name 'Makefile'); do make -f $$i install-deps; done
else
	python utils/install_actor_deps.py $(ACTOR)
endif

install:
	mkdir -p $(ROOT_PATH)
	cp -r src/actors $(ROOT_PATH)
	cp -r src/schemas $(ROOT_PATH)

test:
	python utils/run_pytest.py --actor=$(ACTOR) --report=$(REPORT)



.PHONY: clean install test install-deps build
