PYTHON = uv run python
MANAGE = $(PYTHON) manage.py

.PHONY: help run migrate migrations superuser shell check-db ruff format clean

run:
	$(MANAGE) runserver

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

ruff:
	uv run ruff check

format:
	uv run ruff format

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete