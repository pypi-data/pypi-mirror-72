
default: test


test:
	PYTHONPATH=.: python3 -m pytest


# Ensure that the package installs with all the right dependencies
# in a new virtual environment and run tests.
test_in_venv:
	(                                           \
		set -e;                                 \
		TMP_DIR=$$(mktemp -d);                  \
		python3 -m venv $$TMP_DIR;              \
		. $$TMP_DIR/bin/activate;               \
		pip install ./;                         \
		pip install pytest;                     \
		pip install pyyaml;						\
		python -m pytest .;                     \
		rm -r "$$TMP_DIR"                       \
	)

publish: test_in_venv
	rm  dist/* ||: # the ||: ignores failures
	pip3 install twine # install twine if we don't have it
	python3 setup.py sdist bdist_wheel
	@echo
	@echo Built the distribution. Uploading the package.
	@echo NOTE: The upload command below asks for username and password.
	@echo Use these credentials:
	@cat ../deploy/secret/pypi_org_credentials.txt | grep -v '^#'

	python3 -m twine upload dist/*
