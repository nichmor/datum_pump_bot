PHONY: test
test:
	coverage run -m pytest && coverage report && coverage xml