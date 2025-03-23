.DEFAULT_GOAL := help

help:
	@echo "Usage: make [target]"
	@echo " make install - Installs pre-commit library"
	@echo " make venv - Creates a virtual environment for the backend"
	@echo " make help - Displays this help message"

install:
	pip install pre-commit=="3.3.3"
	pre-commit clean
	pre-commit install
	

venv:
	cd backend 
	uv sync --frozen --no-cache && chmod +x .venv/bin/activate