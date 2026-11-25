# Respuestas HTTP de la Clase 4

Resultados observados con el cliente de DRF sobre la base local.

| Caso | Código | Significado |
|---|---:|---|
| GET `/api/tasks/` | 200 | Lectura correcta |
| POST válido `/api/tasks/` | 201 | Recurso creado |
| DELETE del recurso creado | 204 | Eliminación correcta sin cuerpo |
| POST sin `title` | 400 | Validación rechazada |
| GET `/api/tasks/999999/` | 404 | Recurso inexistente |
| TRACE `/api/tasks/` | 405 | Método no permitido |

La respuesta del POST inválido usa el formato centralizado `{"error": true, "detail": ...}`. Los códigos 401 y 403 corresponden a autenticación y permisos, que se agregan en las clases siguientes; el 500 describe fallas inesperadas del servidor y no se generó artificialmente.
