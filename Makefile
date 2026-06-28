.PHONY: help install run dev docker-build docker-up docker-down docker-logs test clean lint format

help:
	@echo "Task Manager - Comandos disponibles:"
	@echo ""
	@echo "  make install          - Instalar dependencias Python"
	@echo "  make run              - Ejecutar aplicación localmente"
	@echo "  make dev              - Ejecutar en modo desarrollo con hot-reload"
	@echo "  make docker-build     - Construir imagen Docker"
	@echo "  make docker-up        - Levantar aplicación con Docker Compose"
	@echo "  make docker-down      - Detener aplicación Docker"
	@echo "  make docker-logs      - Ver logs de Docker"
	@echo "  make docker-restart   - Reiniciar contenedores Docker"
	@echo "  make test             - Ejecutar tests"
	@echo "  make lint             - Ejecutar linter (flake8)"
	@echo "  make format           - Formatear código (black)"
	@echo "  make clean            - Limpiar archivos temporales y cache"
	@echo "  make db-reset         - Resetear base de datos"
	@echo ""

install:
	@echo "Instalando dependencias..."
	pip install -r requirements.txt

run:
	@echo "Ejecutando aplicación en puerto 8000..."
	uvicorn main:app --host 0.0.0.0 --port 8000

dev:
	@echo "Ejecutando en modo desarrollo con hot-reload..."
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	@echo "Construyendo imagen Docker..."
	docker-compose build

docker-up:
	@echo "Levantando aplicación con Docker Compose..."
	docker-compose up -d
	@echo "Aplicación corriendo en http://localhost:8000"

docker-down:
	@echo "Deteniendo aplicación Docker..."
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-restart:
	@echo "Reiniciando contenedores Docker..."
	docker-compose restart

docker-dev:
	@echo "Levantando en modo desarrollo con Docker..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

test:
	@echo "Ejecutando tests..."
	pytest tests/ -v --cov=backend --cov-report=term-missing

lint:
	@echo "Ejecutando linter..."
	flake8 backend/ --max-line-length=120 --exclude=__pycache__,*.pyc

format:
	@echo "Formateando código..."
	black backend/ --line-length=120
	isort backend/

clean:
	@echo "Limpiando archivos temporales..."
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

db-reset:
	@echo "Reseteando base de datos..."
	rm -f database/tasks.db
	@echo "Base de datos reseteada. Se recreará automáticamente al iniciar la aplicación."
