# Conversación 10: Fix make test-cov

## Contexto
El usuario preguntó si `make test-cov` ejecuta las mismas pruebas que `make test`. Al revisar el Makefile, se identificó que `make test-cov` tenía un bug: no ignoraba `tests/ui/`, lo que causaría errores porque el contenedor de backend no tiene Playwright instalado.

## Problema Identificado
- `make test` ejecuta: `pytest tests/ -v --ignore=tests/ui`
- `make test-cov` ejecutaba: `pytest tests/ -v --cov=backend --cov-report=term-missing`
- **Faltaba**: `--ignore=tests/ui` en `make test-cov`

## Solución Implementada
Se agregó `--ignore=tests/ui` al comando pytest en el target `test-cov` del Makefile.

### Cambio en Makefile
```makefile
test-cov:
	$(check-env)
	@echo "Ejecutando pruebas con cobertura en Docker..."
	docker compose -f docker-compose.test.yml run --rm test pytest tests/ -v --ignore=tests/ui --cov=backend --cov-report=term-missing
	docker compose -f docker-compose.test.yml down -v
```

## Verificación
Se ejecutó `make test-cov` y confirmó:
- ✅ 64 tests pasaron (mismas pruebas que `make test`)
- ✅ 97% de cobertura en el backend
- ⚠️ 1 warning (PendingDeprecationWarning de starlette)

## Diferencia entre make test y make test-cov
| Comando | Pruebas | Cobertura |
|---------|---------|-----------|
| `make test` | 64 tests | No |
| `make test-cov` | 64 tests | Sí (97%) |

Ambos comandos:
- Ejecutan las mismas 64 pruebas de backend
- Ignoran `tests/ui/` (pruebas de interfaz con Playwright)
- Se ejecutan en Docker

## Commit
- **Hash**: `7b5e1f7`
- **Mensaje**: "fix: make test-cov ahora ignora tests/ui"
- **Archivos modificados**: `Makefile`
