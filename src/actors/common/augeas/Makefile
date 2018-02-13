install-deps:
	yum -y install augeas augeas-libs libffi-devel
	pip install python-augeas

test:
	# need to run test_schema.py first, fix this
	pytest ../../../../tests/test_schema.py tests
