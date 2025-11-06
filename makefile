install:
	echo "[Info] - Creating virtualenv"; \
	python3 -m venv .venv; \
	echo "[Info] - Activating virtualenv"; \
	. .venv/bin/activate; \
	echo "[Info] - Installing requirements"; \
	pip3 install -r requirements.txt; \
	echo "Done"; \
	echo "[Info] - Run Unit Tests (pytest)"; \
	pytest; \
	echo "Docker-compose down and up"; \
	docker-compose down && docker-compose up -d; \
	echo "cd services/nuxt3-shadcn && yarn install && yarn dev --open"; \
	cd services/nuxt3-shadcn && yarn install && yarn dev --open; \
	echo "Done"; \

uninstall:
	echo "[Info] - Removing virtualenv"; \
	rm -rf .venv; \
	echo "Done"; \

reinstall:
	echo "[Info] - Reinstalling project"; \
	make uninstall; \
	make install; \
	echo "Done"; \

upgrade:
	echo "[Info] - Upgrading project"; \
	pip3 install -r requirements.txt --upgrade; \
	echo "Done"; \

freeze:
	echo "[Info] - Backing up requirements"; \
	mkdir -p .backups; \
	cp requirements.txt .backups/requirements.txt; \
	echo "[Info] - Freezing project"; \
	pip3 freeze > requirements.txt; \
	echo "Done"; \

test:
	echo "[Info] - Running tests"; \
	python3 -m unittest discover -s tests -p 'test_*.py'; \

clean:
	echo "[Info] - This command removes the virtual environment folder, the database file, and the log file. if they exist"; \
	if [ -d "venv" ]; then rm -rf .venv; fi; \
	if [ -f "app/data/Python_SQLite.db" ]; then rm app/data/Python_SQLite.db; fi; \
	if [ -f "app.log" ]; then rm app.log; fi; \
	if [ -d "htmlcov" ]; then rm -rf htmlcov; fi; \
	echo "Done"; \
	
run:
	@echo "[Info] - Running project"
	@python3 app/main.py

coverage:
	@echo "[Info] - Running coverage"
	@python3 -m unittest discover -s tests -p 'test_*.py' -v
	@coverage run -m unittest discover -s tests -p 'test_*.py'
	@coverage html --include app/* --omit tests/*
	@echo "Done"

DIRECTORY=documents/docs
BUILDDIR=$(DIRECTORY)/build
FILENAME=$(DIRECTORY)/HoppyBrew.rmd
BIBFILENAME=documents/bibliography.bib
MARKDOWNDIR=$(DIRECTORY)/chapters_markdown



pdf:
	python3 tools/MarkdownToPdf.py

git:
	git add .
	git commit -m "Update"
	git push

doc: 
	@make pdf
	@make git


all: 
	@echo "[Clean] - Cleaning project"
	@make clean
	@echo "[Install] - Installing project"
	@make install
	@echo "[Test] - Running tests"
	@make test
	@echo "[Coverage] - Running coverage"
	@make coverage
	@echo "[Doc] - Generating documentation"
	@make doc
	@echo "Done"

help:
	@echo "Available commands:"
	@echo ""
	@echo "Basic commands:"
	@echo "  install       - Install project dependencies"
	@echo "  test          - Run tests"
	@echo "  clean         - Clean project (remove venv, db files, logs)"
	@echo "  run           - Run project"
	@echo "  coverage      - Run coverage"
	@echo "  doc           - Generate documentation"
	@echo "  all           - Run all commands (clean, install, test, coverage, doc)"
	@echo ""
	@echo "Docker commands:"
	@echo "  docker-build    - Build Docker containers"
	@echo "  docker-up       - Start Docker containers"
	@echo "  docker-down     - Stop Docker containers"
	@echo "  docker-restart  - Restart Docker containers"
	@echo "  docker-logs     - Show Docker logs"
	@echo "  docker-clean    - Remove containers, networks, and volumes"
	@echo ""
	@echo "Backend commands:"
	@echo "  backend-test    - Run backend tests"
	@echo "  backend-lint    - Lint backend code"
	@echo "  backend-format  - Format backend code"
	@echo ""
	@echo "Frontend commands:"
	@echo "  frontend-install - Install frontend dependencies"
	@echo "  frontend-dev     - Run frontend in development mode"
	@echo "  frontend-build   - Build frontend"
	@echo "  frontend-lint    - Lint frontend code"
	@echo ""
	@echo "Database migration commands:"
	@echo "  db-migrate      - Create new migration (use msg='description')"
	@echo "  db-upgrade      - Upgrade database to latest migration"
	@echo "  db-downgrade    - Downgrade database by one migration"

requirements:
	@echo "[Info] - Installing requirements"
	@pip3 install -r requirements.txt
	@echo "Done"

# Docker-specific commands
.PHONY: docker-build docker-up docker-down docker-restart docker-logs docker-clean

docker-build:
	@echo "[Info] - Building Docker containers"
	docker-compose build
	@echo "Done"

docker-up:
	@echo "[Info] - Starting Docker containers"
	docker-compose up -d
	@echo "Done"

docker-down:
	@echo "[Info] - Stopping Docker containers"
	docker-compose down
	@echo "Done"

docker-restart:
	@echo "[Info] - Restarting Docker containers"
	docker-compose restart
	@echo "Done"

docker-logs:
	@echo "[Info] - Showing Docker logs"
	docker-compose logs -f

docker-clean:
	@echo "[Info] - Removing Docker containers, networks, and volumes"
	docker-compose down -v
	@echo "Done"

# Backend-specific commands
.PHONY: backend-test backend-lint backend-format

backend-test:
	@echo "[Info] - Running backend tests"
	cd services/backend && python -m pytest
	@echo "Done"

backend-lint:
	@echo "[Info] - Linting backend code"
	cd services/backend && python -m flake8 .
	@echo "Done"

backend-format:
	@echo "[Info] - Formatting backend code"
	cd services/backend && python -m black .
	@echo "Done"

# Frontend-specific commands
.PHONY: frontend-install frontend-dev frontend-build frontend-lint

frontend-install:
	@echo "[Info] - Installing frontend dependencies"
	cd services/nuxt3-shadcn && yarn install
	@echo "Done"

frontend-dev:
	@echo "[Info] - Running frontend in development mode"
	cd services/nuxt3-shadcn && yarn dev

frontend-build:
	@echo "[Info] - Building frontend"
	cd services/nuxt3-shadcn && yarn build
	@echo "Done"

frontend-lint:
	@echo "[Info] - Linting frontend code"
	cd services/nuxt3-shadcn && yarn lint
	@echo "Done"

# Database migration commands
.PHONY: db-migrate db-upgrade db-downgrade

db-migrate:
	@echo "[Info] - Creating new database migration"
	cd services/backend && alembic revision --autogenerate -m "$(msg)"
	@echo "Done"

db-upgrade:
	@echo "[Info] - Upgrading database to latest migration"
	cd services/backend && alembic upgrade head
	@echo "Done"

db-downgrade:
	@echo "[Info] - Downgrading database by one migration"
	cd services/backend && alembic downgrade -1
	@echo "Done"