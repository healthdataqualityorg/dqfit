format:
	black .
	isort .

static-test:
	black --check .
	isort --check --df .
	flake8
	# mypy --strict src tests

pytest:
	# TODO: Report error when coverage < 90% (using --cov-fail-under=90)
	pytest --cov=src --cov-report=term --durations=3 --cache-clear tests

test: static-test pytest
