# Simple makefile with shortcuts to some common tasks

all:
	@echo Supported targets: req test cov

req:
	pip freeze \
		| sed -e '/=0\.0\.0$$/d' -e '/^-e/d' \
		| LC_COLLATE=C sort \
		> requirements.txt

test:
	coverage run -m pytest

cov: test
	coverage report -m
