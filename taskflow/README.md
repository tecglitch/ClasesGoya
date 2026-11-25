# TaskFlow

Backend Django que se construye clase a clase. En Windows PowerShell, activar `venv` con `.\venv\Scripts\Activate.ps1` y correr `python manage.py runserver`. Desde la Clase 9, el comando usa Daphne/ASGI para HTTP y WebSockets.

## Rutas

- Públicas: `/api/health/`, `/api/health/version/`, `POST /api/register/`, `POST /api/token/` y `POST /api/token/refresh/`.
- Protegidas: `/api/projects/`, `/api/projects/<id>/`, `/api/projects/<id>/summary/`, `/api/projects/<id>/add_member/`, `/api/tasks/`, `/api/tasks/<id>/complete/` y `/api/tasks/overdue/`.
- Login social: `/accounts/google/login/`; al volver, JWT en `/api/auth/social/jwt/`.
- GraphQL: `POST /graphql/` con el mismo header `Authorization: Bearer <access>`; GraphiQL está disponible en modo `DEBUG`.
- WebSocket: `ws://127.0.0.1:8000/ws/projects/<id>/`.

## Clases 2 a 12

La base se inicia con `python manage.py migrate`. `python manage.py import_tasks` carga seis registros de prueba desde cuatro proveedores y omite la fila sin título.

Los modelos `Project`, `Task` y `Tag` son relacionales. DRF ofrece CRUD, permisos por membresía, validación, paginación, filtros, sanitización y límites de peticiones. Los servicios gestionan completar/vencidas, resumen y consulta de feriados con caché. El login JWT es independiente del login social.

Channels/Daphne usa Redis como channel layer compartido. Los WebSockets exigen access JWT y membresía al proyecto, publican presencia online/offline y reciben avisos `task_created`, `task_updated` y `task_completed`. Si Redis no está disponible, las tareas siguen guardándose y el fallo de notificación se registra en el log.

Para levantar Redis local, usar Docker si está instalado (`docker run -d --name taskflow-redis -p 6379:6379 redis:7`) o Redis en WSL2. Configurar `REDIS_URL` en `.env` si el servicio escucha en otra dirección. Confirmar con `redis-cli ping` (debería responder `PONG`) antes de iniciar Daphne.

Un cliente WebSocket de ejemplo con reconexión, backoff exponencial, jitter y resincronización está en `docs/cliente_websocket.js`.

GraphQL comparte autenticación JWT, reglas de membresía, validaciones de `TaskSerializer` y notificaciones con REST. Consultas y respuestas del cuestionario de esta unidad están en `docs/respuestas_clase11.md`.

## Pruebas y despliegue (Clase 12)

Ejecutar `pytest` o `pytest --cov=core`. La suite actual tiene 9 pruebas; el último reporte alcanzó 62% de cobertura de líneas en `core`. GitHub Actions corre las pruebas para `push` y `pull_request` a `main` (workflow en `.github/workflows/ci.yml`). Para construir con Docker se necesita un `.env.docker` local, ignorado por Git; pasos y límites del despliegue están en `docs/despliegue_clase12.md`.

## Seguridad y configuración

CORS permite `http://localhost:3000` y `https://taskflow-app.com`. Login fallido y escritura denegada se auditan en DB y `security.log`. Las descripciones se limpian con `nh3`. `SECRET_KEY` y credenciales OAuth se leen desde `.env`; los secretos y artefactos locales están en `.gitignore`.

Allauth está configurado, pero el login de Google requiere Client ID y Secret creados en Google Cloud y cargados en `.env`.

- Flujo OAuth: `docs/oauth_flujo.md`.
- Auditoría de seguridad: `docs/auditoria_seguridad.md`.
- Resultados HTTP de Clase 4: `data/respuestas_http_clase4.md`.
