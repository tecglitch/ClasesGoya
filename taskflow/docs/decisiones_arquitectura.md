# Decisiones de arquitectura — TaskFlow

## Organización del sistema

TaskFlow está construido como una aplicación Django modular. Django REST Framework ofrece la API principal para operaciones de proyectos y tareas. El modelo relacional concentra la fuente de verdad: proyectos, tareas, etiquetas y membresías están relacionados en la base de datos. Un repositorio agrupa consultas frecuentes y los servicios reúnen reglas de negocio como completar tareas, resumir proyectos, consultar feriados y notificar cambios. Esta separación permite que las vistas REST y GraphQL compartan reglas sin duplicarlas.

REST conserva rutas por recurso y códigos HTTP, que son sencillos de integrar y cachear. GraphQL se suma como una segunda forma de consulta para pantallas que necesitan relaciones y campos distintos; expone solo campos elegidos y filtra por membresía. Sus mutations reutilizan el serializer, los permisos y las notificaciones del backend REST. La decisión evita mantener dos implementaciones independientes del dominio.

## Acceso y seguridad

La API usa JWT para autenticación y membresías para autorización. Los usuarios solo listan proyectos y tareas de los que son miembros, y solo admins pueden escribir. El login social se configura aparte del flujo JWT normal. Se agregaron límites de peticiones, limpieza de HTML, CORS acotado y registro de acciones de seguridad. Los WebSockets validan un access JWT y la membresía antes de unirse al grupo del proyecto.

## Actualización en tiempo real

Channels entrega broadcast y presencia online/offline. Redis funciona como channel layer compartido para que distintas instancias de Django vean los mismos grupos; en pruebas se usa `InMemoryChannelLayer`. Las notificaciones son efímeras y se envían después de guardar. Si no llegan, la base sigue siendo la fuente de verdad y el cliente resincroniza con REST al reconectar. Esto mantiene simple el camino crítico de escritura, aunque no ofrece una cola durable de eventos.

## Datos e integración externa

SQLite hace fácil ejecutar el proyecto localmente. Para Docker y producción se configura PostgreSQL mediante variables de entorno. Redis también se configura por ambiente. La API de feriados se consulta a través de un servicio con caché y manejo de fallas: una interrupción externa no impide usar las tareas. Los valores secretos quedan en archivos locales ignorados por Git o en el panel de la plataforma, nunca en el código.

## Calidad y entrega

pytest cubre reglas unitarias y flujos de integración; las dependencias externas se reemplazan por stubs o fakes para que las pruebas sean rápidas y repetibles. GitHub Actions ejecuta las pruebas y la cobertura ante cambios dirigidos a `main`. Docker y Compose describen una topología local con Daphne, PostgreSQL y Redis; WhiteNoise sirve archivos estáticos. El despliegue cloud queda preparado, pero depende de publicar primero el repositorio y configurar servicios y secretos externos.

## Costos de las decisiones

El monolito permite aprender y mantener el sistema con pocas piezas operativas; el límite es que todas las capacidades comparten un mismo despliegue. REST y GraphQL cubren necesidades diferentes, pero GraphQL requiere proteger profundidad, coste e introspección. Redis ofrece coordinación en vivo, no historial durable. SQLite facilita el desarrollo, mientras que PostgreSQL debe probarse en un entorno Docker/producción para detectar diferencias de motor. La suite llegó a 62% de cobertura en `core`; conviene ampliar pruebas de WebSockets, permisos y errores antes de usar el sistema con usuarios reales.
