# TaskFlow Frontend

Sitio estático en HTML, CSS y JavaScript sin frameworks. Consume la API de `../taskflow`.

## Ejecutar en local

1. Levantá el backend TaskFlow en `127.0.0.1:8000` y asegurate de tener Redis activo para las notificaciones en tiempo real.
2. Desde esta carpeta ejecutá `python -m http.server 5500 --bind 127.0.0.1`.
3. Abrí `http://127.0.0.1:5500/` e ingresá con una cuenta registrada.

La sesión y el refresh token se guardan en `sessionStorage`, que se borra al cerrar la pestaña o al salir. La lista permite paginar; el selector cambia el proyecto que escucha el WebSocket. El navegador crea elementos y muestra los datos con `textContent`.
