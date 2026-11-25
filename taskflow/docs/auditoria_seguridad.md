# Revisión de seguridad de TaskFlow

| Área | Resultado actual |
|---|---|
| Control de acceso roto | Las tareas y proyectos se limitan por membresía; los miembros pueden leer, los admins modifican. Un no miembro recibe 404. |
| Contraseñas y tokens | Django hashea contraseñas; la API usa JWT con vencimiento; refresh/login requieren credenciales. |
| Inyección SQL | Consultas realizadas con ORM parametrizado; no se concatena SQL crudo. |
| XSS | `TaskSerializer` limpia `description` con `nh3` y permite cero etiquetas. El frontend futuro también debe escapar al renderizar. |
| Fuerza bruta | Login: cinco intentos por minuto y luego 429; intentos fallidos se registran en `SecurityLog` y `security.log`. |
| Abuso de API | Usuarios anónimos: 20/min; autenticados: 100/min; listados paginados y filtros explícitos. |
| CORS | Solo `http://localhost:3000` y `https://taskflow-app.com`; no se habilita `*`. |
| Secretos | `SECRET_KEY` y credenciales OAuth se leen de `.env`; `.env`, bases y logs están en `.gitignore`. |
| Auditoría | Login fallido y permisos de escritura denegados se guardan en DB y/o log local, sin guardar contraseñas. |
| HTTPS | La configuración local usa HTTP para desarrollo. HTTPS, cookies seguras, `DEBUG=False` y revisión `check --deploy` quedan para despliegue (Clase 12). |

## Verificaciones de la clase

- Login inválido: 401 en los primeros cinco intentos; 429 en el sexto; cinco registros de auditoría.
- Preflight desde `http://localhost:3000`: respuesta con `Access-Control-Allow-Origin`; origen no autorizado: sin ese header.
- Sanitización de `<script>alert(1)</script>Hola <b>mundo</b>`: `Hola mundo`.
- Intento de escritura de un miembro: 403 y registro `permission_denied`.

Las credenciales reales de Google siguen vacías en `.env` hasta crear la aplicación OAuth.
