# Task Manager - Gestor de Tareas

Aplicación web completa para gestión de tareas con autenticación de usuarios, persistencia en base de datos local y despliegue con Docker.

## Características

- **Autenticación de usuarios**: Registro e inicio de sesión con JWT
- **Gestión completa de tareas**: Crear, leer, actualizar y eliminar tareas
- **Propiedades de tareas**: Título, descripción, prioridad (alta/media/baja), estado (pendiente/completada), fecha límite
- **Filtros y búsqueda**: Filtrar por estado y prioridad, buscar por texto, ordenar por múltiples criterios
- **Persistencia de datos**: Base de datos SQLite local
- **Seguridad**: Contraseñas hasheadas con bcrypt, tokens JWT con expiración
- **Diseño responsivo**: Interfaz adaptable a dispositivos móviles y desktop
- **Docker**: Despliegue containerizado con volúmenes persistentes

## Requisitos Iniciales

Antes de ejecutar el proyecto, asegúrate de tener instalado:

| Requisito | Versión mínima | Verificación |
|-----------|---------------|--------------|
| **Docker** | 20.10+ | `docker --version` |
| **Docker Compose** | 2.0+ | `docker compose version` |
| **Make** | 3.81+ | `make --version` |
| **Puerto 8000** | Libre | `lsof -i :8000` |

> **Nota:** No es necesario instalar Python ni dependencias manualmente; Docker se encarga de todo.

## Instrucciones de Ejecución con Make

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd ia2_actividad_1
```

### 2. Configurar variables de entorno
```bash
make env-setup
```
Esto crea un archivo `.env` desde `.env.example`. Edita el archivo para ajustar las variables según tu entorno.

### 3. Levantar la aplicación (producción)
```bash
make docker-up
```
Esto construye la imagen (incluyendo los últimos cambios) y levanta el contenedor en segundo plano. La aplicación estará disponible en **http://localhost:8000**.

### 4. Levantar sin reconstruir (rápido)
```bash
make docker-up-fast
```
Levanta la aplicación sin reconstruir la imagen. Úsalo cuando no hayas hecho cambios en el código.

### 5. Levantar en modo desarrollo (hot-reload)
```bash
make docker-dev
```
Ideal para desarrollo: los cambios en el código se reflejan automáticamente sin reiniciar.

### 5. Levantar en modo desarrollo (hot-reload)
```bash
make docker-dev
```
Ideal para desarrollo: los cambios en el código se reflejan automáticamente sin reiniciar.

### 6. Ver logs en tiempo real
```bash
make docker-logs
```
Presiona `Ctrl+C` para salir de los logs sin detener la aplicación.

### 7. Detener la aplicación
```bash
make docker-down
```

### 8. Reiniciar contenedores
```bash
make docker-restart
```

### 9. Limpiar todo (contenedores, volúmenes y caché)
```bash
make clean
```

### 10. Resetear la base de datos
```bash
make db-reset
```
Elimina `tasks.db`. La base se recrea automáticamente al reiniciar la aplicación.

### Resumen rápido
```bash
make help              # Ver todos los comandos disponibles
make env-setup         # Crear archivo .env desde .env.example
make docker-build      # Solo construir la imagen
make docker-up         # Construir + levantar (reconstruye imagen)
make docker-up-fast    # Solo levantar (sin reconstruir)
make docker-dev        # Modo desarrollo con hot-reload
make docker-logs       # Ver logs
make docker-down       # Detener
make docker-restart    # Reiniciar
make clean             # Limpieza completa
make db-reset          # Resetear base de datos
make test              # Ejecutar pruebas de backend (64 tests)
make test-ui           # Ejecutar pruebas de interfaz web (26 tests)
make test-cov          # Ejecutar pruebas con cobertura
```

## Uso

### Registro de Usuario

1. Acceder a http://localhost:8000
2. Hacer clic en "Regístrate"
3. Completar el formulario con usuario, email y contraseña (mínimo 6 caracteres)
4. Hacer clic en "Registrarse" o presionar **Enter**

### Inicio de Sesión

1. Ingresar email y contraseña
2. Hacer clic en "Iniciar Sesión" o presionar **Enter**

### Gestión de Tareas

#### Crear una tarea
1. Hacer clic en "+ Nueva Tarea"
2. Completar el formulario:
   - **Título** (obligatorio)
   - **Descripción** (opcional)
   - **Prioridad**: Alta, Media, Baja
   - **Fecha límite** (opcional)
3. Hacer clic en "Guardar" o presionar **Enter**

#### Editar una tarea
1. Hacer clic en "Editar" en la tarea deseada
2. Modificar los campos necesarios
3. Hacer clic en "Guardar"

#### Cambiar estado de tarea
- Hacer clic en "Completar" o "Reabrir" para cambiar el estado

#### Eliminar una tarea
1. Hacer clic en "Eliminar"
2. Confirmar la eliminación en el diálogo

### Filtros y Búsqueda

- **Buscar**: Escribir en el campo de búsqueda (busca en título y descripción)
- **Filtrar por estado**: Seleccionar "Pendientes", "Completadas" o "Todos"
- **Filtrar por prioridad**: Seleccionar "Alta", "Media", "Baja" o "Todas"
- **Ordenar**: Seleccionar criterio (Más recientes, Más antiguas, Fecha límite, Prioridad, Título)
- **Limpiar filtros**: Hacer clic en "Limpiar" para resetear todos los filtros

### Cerrar Sesión

Hacer clic en "Cerrar Sesión" en la esquina superior derecha

## API Documentation

La API incluye documentación interactiva automática:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Endpoints de Autenticación

#### POST /api/auth/register
Registro de nuevo usuario

**Request:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores:**
- 400: Username already registered / Email already registered

#### POST /api/auth/login
Inicio de sesión

**Request:**
```json
{
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores:**
- 401: Invalid email or password

### Endpoints de Tareas

Todos los endpoints de tareas requieren autenticación JWT. Incluir el token en el header:
```
Authorization: Bearer <access_token>
```

#### POST /api/tasks/
Crear nueva tarea

**Request:**
```json
{
  "title": "Completar proyecto",
  "description": "Finalizar la aplicación web",
  "priority": "high",
  "due_date": "2026-07-01"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Completar proyecto",
  "description": "Finalizar la aplicación web",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-07-01",
  "created_at": "2026-06-27T10:30:00",
  "updated_at": null,
  "user_id": 1
}
```

**Errores:**
- 400: Title is required / Priority must be low, medium, or high
- 401: Not authenticated

#### GET /api/tasks/
Listar todas las tareas del usuario autenticado

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Completar proyecto",
    "description": "Finalizar la aplicación web",
    "status": "pending",
    "priority": "high",
    "due_date": "2026-07-01",
    "created_at": "2026-06-27T10:30:00",
    "updated_at": null,
    "user_id": 1
  }
]
```

#### GET /api/tasks/{task_id}
Obtener tarea específica

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Completar proyecto",
  "description": "Finalizar la aplicación web",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-07-01",
  "created_at": "2026-06-27T10:30:00",
  "updated_at": null,
  "user_id": 1
}
```

**Errores:**
- 404: Task not found

#### PUT /api/tasks/{task_id}
Actualizar tarea

**Request:**
```json
{
  "title": "Proyecto completado",
  "status": "completed",
  "priority": "high"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Proyecto completado",
  "description": "Finalizar la aplicación web",
  "status": "completed",
  "priority": "high",
  "due_date": "2026-07-01",
  "created_at": "2026-06-27T10:30:00",
  "updated_at": "2026-06-27T11:00:00",
  "user_id": 1
}
```

**Errores:**
- 400: Title cannot be empty / Status must be pending or completed
- 404: Task not found

#### DELETE /api/tasks/{task_id}
Eliminar tarea

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

**Errores:**
- 404: Task not found

## Capturas de Pantalla

### Pantalla de Login
![Login](docs/screenshots/login.png)

### Pantalla de Registro
![Registro](docs/screenshots/registro.png)

### Lista de Tareas y Filtros
![Lista de Tareas](docs/screenshots/lista_tareas_y_filtros.png)

### Crear Nueva Tarea
![Nueva Tarea](docs/screenshots/nueva_tarea.png)

### Selector de Fecha
![Datepicker](docs/screenshots/nueva_tarea_datepicker.png)

## Troubleshooting

### Error: "Port 8000 already in use"
**Solución**: Detener otra aplicación que use el puerto 8000 o cambiar el puerto:
```bash
uvicorn main:app --port 8001
```

### Error: "ModuleNotFoundError: No module named 'fastapi'"
**Solución**: Activar el entorno virtual e instalar dependencias:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Database locked"
**Solución**: SQLite no soporta múltiples escrituras simultáneas. Cerrar otras instancias de la aplicación.

### Error de Docker: "Cannot connect to the Docker daemon"
**Solución**: Iniciar Docker Desktop o el servicio Docker:
```bash
sudo systemctl start docker  # Linux
# o iniciar Docker Desktop en macOS/Windows
```

### Error de Docker: "Port 8000 is already in use"
**Solución**: Cambiar el puerto en docker-compose.yml:
```yaml
ports:
  - "8001:8000"
```

### Los datos se pierden al reiniciar Docker
**Solución**: Verificar que el volumen esté configurado correctamente en docker-compose.yml:
```yaml
volumes:
  - db_data:/app/database
```

### Error de autenticación: "Token has expired"
**Solución**: El token JWT expira después de 30 minutos. Iniciar sesión nuevamente para obtener un nuevo token.

### Error: "Invalid token"
**Solución**: El token puede estar corrupto o ser inválido. Cerrar sesión e iniciar nuevamente.

## Estructura del Proyecto

```
ia2_actividad_1/
├── backend/
│   ├── __init__.py
│   ├── auth.py              # Autenticación JWT y hashing
│   ├── database.py          # Configuración de base de datos
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Esquemas Pydantic
│   └── routers/
│       ├── auth.py          # Endpoints de autenticación
│       └── tasks.py         # Endpoints de tareas
├── frontend/
│   ├── index.html           # Interfaz web
│   ├── styles.css           # Estilos CSS
│   ├── auth.js              # Lógica de autenticación
│   ├── api.js               # Llamadas a API
│   └── app.js               # Lógica de la aplicación
├── database/                # Base de datos SQLite (generado)
├── main.py                  # Punto de entrada FastAPI
├── Makefile                 # Comandos rápidos de desarrollo
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Configuración Docker
├── docker-compose.yml       # Orquestación Docker
├── docker-compose.dev.yml   # Configuración desarrollo
├── .env                     # Variables de entorno
└── README.md                # Este archivo
```

## Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos local
- **Pydantic**: Validación de datos
- **python-jose**: Manejo de tokens JWT
- **passlib**: Hashing de contraseñas con bcrypt

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos responsivos
- **JavaScript (ES6+)**: Lógica de la aplicación
- **Fetch API**: Llamadas HTTP

### Despliegue
- **Docker**: Containerización
- **Docker Compose**: Orquestación de contenedores

## Limitaciones Conocidas

1. **SQLite**: No diseñado para alto tráfico concurrente
2. **JWT en localStorage**: Vulnerable a ataques XSS (aceptable para proyecto académico)
3. **Sin roles de usuario**: Todos los usuarios tienen los mismos permisos
4. **Sin recuperación de contraseña**: No implementado en esta versión
5. **Un solo usuario por tarea**: No hay tareas compartidas

## Trabajo Futuro

- Implementar recuperación de contraseña
- Añadir roles de usuario (admin/user)
- Soporte para tareas compartidas
- Exportación de tareas a CSV/PDF
- Notificaciones por email
- API REST completa con paginación
- Despliegue en producción con base de datos PostgreSQL

## Actividad 2 - Creación de Pruebas

### Resumen de Pruebas

El proyecto cuenta con un entorno completo de pruebas automatizadas que cubren todas las funcionalidades clave de la aplicación. Todas las pruebas se ejecutan en contenedores Docker, sin requerir instalación de dependencias en el host.

**Total de pruebas: 90 tests**
- ✅ Backend: 64 tests (97% cobertura)
- ✅ Frontend: 26 tests de interfaz web

### Tipos de Pruebas

#### 1. Pruebas Unitarias (28 tests)
Validan funciones individuales y validación de modelos Pydantic.

**Ubicación:** `tests/unit/`

- **test_auth.py** (9 tests): Hashing de contraseñas, creación y verificación de tokens JWT
- **test_schemas.py** (19 tests): Validación de esquemas Pydantic (UserRegister, UserLogin, TaskCreate, TaskUpdate)

#### 2. Pruebas de Integración (30 tests)
Validan los endpoints de la API y su interacción con la base de datos.

**Ubicación:** `tests/integration/`

- **test_auth_api.py** (10 tests): Endpoints de autenticación (registro, login, errores)
- **test_tasks_api.py** (20 tests): Endpoints de tareas (CRUD, autorización, aislamiento entre usuarios)

#### 3. Pruebas End-to-End (6 tests)
Validan flujos completos de usuario a través de múltiples operaciones.

**Ubicación:** `tests/e2e/`

- **test_workflows.py** (6 tests): Ciclo de vida completo, múltiples tareas, aislamiento entre usuarios, reutilización de tokens, acceso no autenticado

#### 4. Pruebas de Interfaz Web (26 tests)
Validan la interfaz de usuario usando Playwright para automatización de navegador.

**Ubicación:** `tests/ui/`

- **test_interface.py** (26 tests):
  - TestAuthUI (10 tests): Login, registro, validaciones, logout
  - TestTasksUI (16 tests): Elementos principales, creación/edición/eliminación de tareas, filtros, búsqueda

### Ejecución de Pruebas

```bash
# Ejecutar pruebas de backend (64 tests)
make test

# Ejecutar pruebas de interfaz web (26 tests)
make test-ui

# Ejecutar pruebas de backend con reporte de cobertura
make test-cov
```

Todas las pruebas se ejecutan en contenedores Docker aislados. No se requiere Python ni dependencias instaladas en el host.

### Historial de Conversaciones

A continuación se documentan las conversaciones realizadas durante el desarrollo de la Actividad 2, con enlaces a los resúmenes detallados:

| # | Commit | Descripción | Documentación |
|---|--------|-------------|---------------|
| 1 | `16f6b89` | Entorno completo de pruebas Docker + Corrección de warnings | [conversation-summary.md](docs/conversation-summary.md) |
| 2 | `a350a7a` | .venv/ al .gitignore y remover del tracking | [conversation-summary.md](docs/conversation-summary.md) |
| 3 | `c48d440` | .env.example y target make env-setup | [conversation-summary.md](docs/conversation-summary.md) |
| 4 | `264bd01` | Validar existencia de .env en docker-up | [conversation-summary.md](docs/conversation-summary.md) |
| 5 | `e8db7ec` | Validar .env en todos los targets que lo requieren | [conversation-summary.md](docs/conversation-summary.md) |
| 6 | `95302a2` | Actualización de pytest y verificación de pruebas | [conversation-summary-2.md](docs/conversation-summary-2.md) |
| 7 | `d8d9167` | Pruebas de interfaz web con Playwright (26 tests) | [conversation-summary-4.md](docs/conversation-summary-4.md) |
| 8 | `5f86fac` | Excluir tests/ui de make test | [conversation-summary-4.md](docs/conversation-summary-4.md) |
| 9 | `adc90cf` | Formularios de login y registro se envían con Enter | [conversation-summary-5.md](docs/conversation-summary-5.md) |
| 10 | `50cb848` | docker-up ahora reconstruye la imagen automáticamente | [conversation-summary-6.md](docs/conversation-summary-6.md) |
| 11 | `fa1ff86` | Modal de Nueva Tarea y búsqueda se envían con Enter | [conversation-summary-7.md](docs/conversation-summary-7.md) |
| 12 | `d840f49` | Actualizar README con mejoras y sección Actividad 2 | [conversation-summary-8.md](docs/conversation-summary-8.md) |
| 13 | `93bdbef` | Agregar nota sobre placeholder de hash en historial | [conversation-summary-9.md](docs/conversation-summary-9.md) |
| 14 | `VER HISTORIAL` | Fix make test-cov ignora tests/ui | [conversation-summary-10.md](docs/conversation-summary-10.md) |

> **Nota:** El hash del último commit se actualiza en la siguiente interacción para evitar bucles infinitos de actualización. Consulta `git log` para ver el hash actualizado.

### Mejoras Realizadas

Durante el desarrollo de la Actividad 2, se realizaron las siguientes mejoras adicionales:

1. **Corrección de warnings de deprecación**
   - SQLAlchemy: `declarative_base()` movido a `sqlalchemy.orm`
   - Pydantic V2: `class Config` reemplazado por `model_config = ConfigDict()`
   - Pydantic V2: `.dict()` reemplazado por `.model_dump()`
   - FastAPI: `@app.on_event("startup")` reemplazado por `lifespan`
   - passlib: Reemplazado por `bcrypt` directo

2. **Mejoras de UX en formularios**
   - Formularios de login y registro ahora se envían con Enter
   - Modal de Nueva Tarea se envía con Enter
   - Input de búsqueda acepta Enter para quitar el foco

3. **Mejoras en el flujo de desarrollo**
   - `make docker-up` ahora reconstruye la imagen automáticamente
   - Nuevo comando `make docker-up-fast` para levantados rápidos
   - Validación de `.env` en todos los targets que lo requieren

### Cobertura de Código

El entorno de pruebas alcanza un **97% de cobertura** en el código backend:

```
Name                          Stmts   Miss  Cover
--------------------------------------------------
backend/__init__.py               0      0   100%
backend/auth.py                  49      4    92%
backend/database.py              13      4    69%
backend/models.py                21      0   100%
backend/routers/__init__.py       0      0   100%
backend/routers/auth.py          29      0   100%
backend/routers/tasks.py         44      0   100%
backend/schemas.py               84      0   100%
--------------------------------------------------
TOTAL                           240      8    97%
```

## Licencia

Proyecto académico desarrollado para la asignatura de Desarrollo de Aplicaciones con Asistentes de Programación basados en IA.

## Contacto

Para dudas o comentarios sobre el proyecto, contactar al equipo de desarrollo.
