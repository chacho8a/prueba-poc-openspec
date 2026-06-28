.PHONY: help docker-build docker-up docker-down docker-logs docker-restart docker-dev test test-cov env-setup clean db-reset

help:
	@echo "Task Manager - Comandos disponibles:"
	@echo ""
	@echo "  make docker-build     - Construir imagen Docker"
	@echo "  make docker-up        - Levantar aplicación con Docker Compose"
	@echo "  make docker-down      - Detener aplicación Docker"
	@echo "  make docker-logs      - Ver logs de Docker"
	@echo "  make docker-restart   - Reiniciar contenedores Docker"
	@echo "  make docker-dev       - Levantar en modo desarrollo con hot-reload"
	@echo "  make test             - Ejecutar pruebas en Docker"
	@echo "  make test-cov         - Ejecutar pruebas con cobertura en Docker"
	@echo "  make env-setup        - Crear archivo .env desde .env.example"
	@echo "  make clean            - Limpiar archivos temporales y cache"
	@echo "  make db-reset         - Resetear base de datos"
	@echo ""

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
	@echo "Ejecutando pruebas en Docker..."
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker compose -f docker-compose.test.yml down -v

test-cov:
	@echo "Ejecutando pruebas con cobertura en Docker..."
	docker compose -f docker-compose.test.yml run --rm test pytest tests/ -v --cov=backend --cov-report=term-missing
	docker compose -f docker-compose.test.yml down -v

env-setup:
	@if [ -f .env ]; then \
		echo "El archivo .env ya existe. Si deseas recrearlo, elimínalo primero con: rm .env"; \
	else \
		cp .env.example .env && \
		echo "Archivo .env creado desde .env.example"; \
		echo "Edita .env para ajustar las variables de entorno según tu entorno."; \
	fi

clean:
	@echo "Limpiando archivos temporales y contenedores Docker..."
	docker-compose down -v --remove-orphans 2>/dev/null || true
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -f database/tasks.db
	@echo "Limpieza completa: contenedores, volúmenes y archivos temporales eliminados"

db-reset:
	@echo "Reseteando base de datos..."
	rm -f database/tasks.db
	@echo "Base de datos reseteada. Se recreará automáticamente al iniciar la aplicación."
