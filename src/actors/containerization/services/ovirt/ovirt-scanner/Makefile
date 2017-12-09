PHONY: build clean

clean:
	rm -rf actor-sdk
	rm -f leapp
	rm -f _actor.yaml

build:
	git clone https://github.com/leapp-to/actor-sdk
	ln -s actor-sdk/python/leapp leapp
	python actor.py --dump-yaml > _actor.yaml
