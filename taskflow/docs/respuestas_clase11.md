# Clase 11 — Repaso y tarea

## 1. SDL y `[TaskType!]!`

SDL es el lenguaje para describir el esquema GraphQL: tipos, campos, argumentos y operaciones. `[TaskType!]!` representa una lista que no puede ser nula y cuyos elementos tampoco pueden ser nulos.

## 2. Operaciones

`Query` lee, `Mutation` modifica datos y `Subscription` transmite cambios a medida que ocurren. Subscription se relaciona con la Unidad 4 y sus avisos en tiempo real por WebSocket.

## 3. `data` y `errors`

GraphQL resuelve un árbol de campos. Si un campo falla, otros pueden resolverse; por eso una respuesta puede incluir datos parciales y errores a la vez. Habitualmente la respuesta de ejecución usa HTTP 200, así que el cliente también debe revisar `errors`.

## 4. REST y GraphQL: caché, versionado y errores

REST aprovecha caché HTTP por URL, suele versionarse en rutas y comunica errores con estados HTTP. GraphQL concentra operaciones en `/graphql/`, lo que hace más difícil la caché HTTP tradicional; suele agregar campos y marcar los antiguos como obsoletos en lugar de versionar la URL, y devuelve errores en el JSON.

## 5. Ejecución de resolvers

La consulta se resuelve como un árbol: primero el campo raíz, después sus campos anidados para cada objeto padre. `root` contiene el resultado padre; `info.context` comparte el contexto de la petición, incluido el usuario.

## 6. N+1

Una consulta inicial que obtiene proyectos y luego consulta tareas por cada proyecto produce N+1 consultas. En el ejemplo de la guía, 6 proyectos causaban 7 consultas; `prefetch_related("tasks")` las reduce a 2.

## 7. Diseño de mutations

Usar nombres de acción claros, validar entradas, devolver el objeto modificado para que el cliente actualice su vista y comunicar errores de forma consistente. Para entradas extensas, agrupar parámetros en un tipo input.

## 8. Riesgos y mitigaciones

Consultas profundas o costosas pueden consumir recursos; limitar profundidad y costo. La introspección expone el esquema; puede desactivarse en producción. Cada resolver debe respetar autenticación y permisos, y el endpoint debe tener límites de peticiones.

## 9. Integrar otro servicio

Un resolver puede llamar un servicio externo y devolver su resultado como campo. Por ejemplo, un campo `resumenIa` de `ProjectType` podría consultar un servicio de IA para resumir las tareas del proyecto.

## 10. Stitching, federación y gateway

Schema stitching combina en un servidor esquemas existentes y decide cómo relacionarlos. En federación, cada servicio publica un subgrafo con sus entidades; un gateway compone el esquema y reparte cada consulta a los servicios correspondientes.

## Tarea: REST vs GraphQL

Usaría REST para una descarga de archivo o una integración sencilla de terceros: cada recurso tiene URL estable, los códigos HTTP son claros y la caché del navegador o proxy funciona naturalmente. Usaría GraphQL para una pantalla móvil que necesita, en una sola petición, nombre del proyecto, tareas y etiquetas, pero otra pantalla solo requiere títulos: cada cliente pide su forma de datos sin crear endpoints específicos. En TaskFlow ambos conviven y comparten modelos, permisos y validaciones.
