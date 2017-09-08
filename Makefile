clean:
	@rm -rf build/ dist/ *.egg-info
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

install:
	pip install -r requirements.txt

test:
	py.test tests/*.py 

.PHONY: clean install test 
