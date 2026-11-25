# Programación IV

Repositorio de los ejercicios prácticos de la materia, ordenados por clase.

## Proyectos

- `python_backend_tpi/`: ejercicios de Python, CSV, JSON y validación de la Clase 1.
- `taskflow/`: API Django/DRF con PostgreSQL, Redis, WebSockets, GraphQL, pruebas automatizadas y configuración Docker.
- `taskflow-frontend/`: interfaz web estática opcional en HTML, CSS y JavaScript.

## TaskFlow en desarrollo

Desde `taskflow/`, activar el entorno virtual, instalar dependencias y ejecutar migraciones:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Las notificaciones WebSocket requieren Redis. Para el entorno con PostgreSQL y Redis, consultar `taskflow/docs/despliegue_clase12.md`.

Las pruebas se ejecutan con `pytest`; la cobertura se mide con `pytest --cov=core`.

## Frontend opcional

Con el backend activo, desde `taskflow-frontend/` ejecutar:

```powershell
python -m http.server 5500 --bind 127.0.0.1
```

Abrir `http://127.0.0.1:5500/` en el navegador.
