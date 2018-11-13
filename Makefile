.PHONY: init check dist publish

init: req
	pipenv install -e "."
	pipenv run python setup.py develop

check: test
	#pipenv check
	pipenv run pylint setup.py
	#pipenv run pylint tamago/*.py

test: req
	pipenv install -e ".[test]"
	pipenv run python setup.py develop

dist: init check req
	pipenv run python setup.py sdist bdist_wheel install

live:
	pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py
	pip install -e "."

req:
	pipenv run pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py
