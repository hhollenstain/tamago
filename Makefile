.PHONY: init check dist publish

init:
	pipenv install -e "."
	pipenv run python setup.py develop

check: test
	pipenv check
	pipenv run pylint setup.py
	pipenv run pylint tamago/*.py

test:
	pipenv install -e ".[test]"
	pipenv run python setup.py develop

dist: init check
	pipenv run python setup.py sdist bdist_wheel install

publish: check
	pipenv run python setup.py sdist bdist_wheel upload -r artifactory
