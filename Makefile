# Makefile for user-api-fastapi project

.PHONY: help install run test lint format

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  run         Run the FastAPI server (hot reload)"
	@echo "  test        Run all tests with pytest"
	@echo "  lint        Run Ruff linter"
	@echo "  format      Format code with Black and isort"

install:
	poetry install

run:
	poetry run uvicorn main:app --reload

test:
	poetry run pytest -v

lint:
	poetry run ruff .

format:
	poetry run black .
	poetry run isort .


.PHONY: frontend

frontend:
	cd frontend && npm start