.PHONY: install run test clean

install:
	pip install -e '.[dev]'

run:
	python -m src.app

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -f *.db
