.PHONY: test

test:
	coverage run -m pytest
	coverage xml
