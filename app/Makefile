VIRTUALENV="virtualenv"
virtualenv_dir="venv"

setup: venv deps

venv:
	test -d $(virtualenv_dir) || ($(VIRTUALENV) $(virtualenv_dir) || true)
	. $(virtualenv_dir)/bin/activate

deps:
	pip install -Ur requirements_dev.txt

keys:
	python ./application/generate_keys.py

