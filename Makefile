.PHONY: install run solution test lint format clean

install:
	python -m pip install -e ".[dev,notebook]"

solution:          ## the literal answer to the exercise
	python solution.py

run:               ## the engineered version
	python -m iot_monitor

test:
	pytest --cov --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov build dist *.egg-info
	find . -name __pycache__ -type d -exec rm -rf {} +
