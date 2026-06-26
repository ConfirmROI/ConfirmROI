.PHONY: help install dev test test-backend test-frontend build run stop migrate seed lint clean demo-free demo-paid demo-free-reset demo-paid-reset demo-stop demo-free-docker demo-paid-docker demo-free-docker-reset demo-paid-docker-reset demo-docker-stop

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install backend and frontend dependencies
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

dev: ## Start development servers (backend + frontend)
	@echo "Starting backend..."
	cd backend && source venv/bin/activate && flask --app wsgi run --debug &
	@echo "Starting frontend..."
	cd frontend && npm run dev

test-backend: ## Run backend tests
	cd backend && source venv/bin/activate && python -m pytest tests/ -v

test-frontend: ## Run frontend tests
	cd frontend && npm run test

test: test-backend test-frontend ## Run all tests

migrate: ## Run database migrations
	cd backend && source venv/bin/activate && flask --app wsgi db upgrade

seed: ## Seed system archetypes
	cd backend && source venv/bin/activate && python -m app.services.seed

build: ## Build Docker images
	docker compose build

run: ## Start all services via Docker
	docker compose up -d

stop: ## Stop Docker services
	docker compose down

demo-free: ## Start free-tier demo (backend: 5100, frontend: 5174)
	@echo "Seeding free-tier demo data..."
	cd backend && source venv/bin/activate && \
		DATABASE_URL=sqlite:///confirmroi_demo_free.db \
		DEMO_TIER=free DEFAULT_USER_TIER=free \
		python -m app.services.demo_seed
	@echo "Starting free-tier demo backend on :5100..."
	cd backend && source venv/bin/activate && \
		DATABASE_URL=sqlite:///confirmroi_demo_free.db \
		DEMO_TIER=free DEFAULT_USER_TIER=free \
		flask --app wsgi run --port 5100 --debug &
	@echo "Starting free-tier demo frontend on :5174..."
	cd frontend && VITE_PROXY_TARGET=http://localhost:5100 npx vite --port 5174

demo-paid: ## Start paid-tier demo (backend: 5200, frontend: 5175)
	@echo "Seeding paid-tier demo data..."
	cd backend && source venv/bin/activate && \
		DATABASE_URL=sqlite:///confirmroi_demo_paid.db \
		DEMO_TIER=paid DEFAULT_USER_TIER=paid \
		python -m app.services.demo_seed
	@echo "Starting paid-tier demo backend on :5200..."
	cd backend && source venv/bin/activate && \
		DATABASE_URL=sqlite:///confirmroi_demo_paid.db \
		DEMO_TIER=paid DEFAULT_USER_TIER=paid \
		flask --app wsgi run --port 5200 --debug &
	@echo "Starting paid-tier demo frontend on :5175..."
	cd frontend && VITE_PROXY_TARGET=http://localhost:5200 npx vite --port 5175

demo-free-reset: ## Wipe and restart free-tier demo (deletes SQLite DB)
	rm -f backend/confirmroi_demo_free.db
	@$(MAKE) demo-free

demo-paid-reset: ## Wipe and restart paid-tier demo (deletes SQLite DB)
	rm -f backend/confirmroi_demo_paid.db
	@$(MAKE) demo-paid

demo-stop: ## Stop all demo instances
	-pkill -f "flask --app wsgi run --port 5100"
	-pkill -f "flask --app wsgi run --port 5200"
	-pkill -f "vite --port 5174"
	-pkill -f "vite --port 5175"

demo-free-docker: ## Start free-tier demo via Docker (backend: 5100, frontend: 5174)
	docker compose -f docker-compose.demo-free.yml up -d --build

demo-paid-docker: ## Start paid-tier demo via Docker (backend: 5200, frontend: 5175)
	docker compose -f docker-compose.demo-paid.yml up -d --build

demo-free-docker-reset: ## Wipe and restart free-tier Docker demo
	docker compose -f docker-compose.demo-free.yml down -v
	@$(MAKE) demo-free-docker

demo-paid-docker-reset: ## Wipe and restart paid-tier Docker demo
	docker compose -f docker-compose.demo-paid.yml down -v
	@$(MAKE) demo-paid-docker

demo-docker-stop: ## Stop all Docker demo instances
	docker compose -f docker-compose.demo-free.yml down
	docker compose -f docker-compose.demo-paid.yml down

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	rm -rf backend/instance
	rm -rf frontend/dist
