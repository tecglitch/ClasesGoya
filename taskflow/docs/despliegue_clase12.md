# Clase 12 — Ejecución, CI/CD y despliegue

## Tests

El conjunto usa pytest-django, una base de datos temporal, un channel layer en memoria y una lista de feriados controlada. No requiere Redis ni acceso a Internet. Ejecutar `pytest -v` y luego `pytest --cov=core --cov-report=term-missing`.

## Integración continua

`.github/workflows/ci.yml` ejecuta las pruebas en Python 3.12 ante cada `push` o `pull_request` dirigido a `main`. Usa una `SECRET_KEY` ficticia de CI; no carga secretos reales del equipo.

## Docker local

`Dockerfile` arma la imagen de Django/Daphne. `docker-compose.yml` coordina la app, PostgreSQL y Redis; la base persiste en el volumen `pgdata`. Crear `.env.docker` a partir de `.env.example`, con `DEBUG=False`, `DB_ENGINE=postgresql`, `DB_HOST=db`, `REDIS_URL=redis://redis:6379` y una clave secreta propia. El archivo está ignorado por Git y por Docker.

Con Docker Desktop iniciado:

```powershell
docker compose up -d --build
docker compose logs -f web
docker compose exec web python manage.py createsuperuser
docker compose down
```

Verificación adicional: `docker compose exec web python manage.py check --deploy`. Los avisos sobre HTTPS, cookies y HSTS requieren configuración al publicar con un dominio TLS.

## Publicación en la nube

La imagen y las variables ya dejan preparado el despliegue en un PaaS. Publicarlo requiere que el proyecto esté en GitHub y que se creen servicios gestionados de PostgreSQL y Redis, además de configurar variables secretas y el dominio. La publicación en línea queda pendiente; todavía no hay un despliegue online.

## Observabilidad y versionado

En producción, revisar los logs desde la salida estándar/panel de la plataforma; un archivo dentro de un contenedor puede perderse al recrearlo. SemVer: parche para correcciones compatibles (`1.0.0` → `1.0.1`), menor para sumar un campo o endpoint compatible (`1.0.1` → `1.1.0`) y mayor para cambios incompatibles (`1.1.0` → `2.0.0`). Las migraciones necesitan compatibilidad hacia atrás porque volver atrás el código no deshace automáticamente los datos de la base.

