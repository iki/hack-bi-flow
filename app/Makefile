VIRTUALENV="virtualenv"
VIRTUALENV_DIR=".virtualenv"

setup: venv deps

venv:
	test -d $(VIRTUALENV_DIR) || ($(VIRTUALENV) $(VIRTUALENV_DIR) || true)
	. $(VIRTUALENV_DIR)/bin/activate

deps:
	pip install -Ur requirements_dev.txt

keys:
	python ./application/generate_keys.py

