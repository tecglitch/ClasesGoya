# Clase 13 opcional — Repaso

## 1. Separar frontend y backend

Permite desplegar y actualizar la interfaz sin cambiar la API, y hace posible que varios clientes compartan el mismo backend: este frontend, una app móvil, una integración o GraphiQL.

## 2. Renderizado en servidor y SPA

En renderizado de servidor, el backend devuelve HTML ya armado. Una SPA entrega una página inicial y JavaScript actualiza la interfaz y consulta la API sin recargar todo; este ejemplo es mínimo y no usa framework.

## 3. `fetch` y `async/await`

`fetch` no bloquea el hilo visual; devuelve una promesa y `await` pausa solo esa función hasta que llegue la respuesta. Es el mismo estilo de programación asincrónica que usamos con `async/await` en Python/Channels.

## 4. Revisar `response.ok`

Un 401 o 500 es una respuesta HTTP válida, así que `fetch` no rechaza automáticamente la promesa. `response.ok` indica si el estado es 2xx y permite mostrar el error de la API.

## 5. DOM y `textContent`

El DOM representa la página como objetos que JavaScript puede modificar. `textContent` inserta texto literal; `innerHTML` interpreta etiquetas y podría ejecutar contenido malicioso recibido de la API.

## 6. Abrir con doble clic

Con `file://` el origen del navegador es especial y puede bloquear las solicitudes de red. Un servidor HTTP local ofrece un origen permitido por CORS.

## 7. Sitio estático y CDN

Un sitio estático entrega archivos HTML, CSS y JS sin generarlos en cada petición. Una CDN distribuye copias de esos archivos desde servidores cercanos al usuario.
