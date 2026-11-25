# Clase 10 — Repaso y tarea

## 1. Comando y evento

Un comando pide que ocurra algo y puede rechazarse; por ejemplo, `POST /api/tasks/` solicita crear una tarea. Un evento informa que algo ya ocurrió; por ejemplo, `task_created` se publica después de guardar la tarea.

## 2. Publicar/suscribir y cola

En publicar/suscribir, un productor envía un mensaje a un canal y todos los consumidores suscriptos pueden recibirlo. En una cola, normalmente un consumidor toma cada mensaje para procesarlo; esto permite repartir trabajo. Los grupos de Channels son adecuados para avisos en vivo a varias conexiones, no para trabajos durables.

## 3. Entrega del channel layer

El channel layer ofrece entrega como máximo una vez. Una notificación puede perderse si el usuario está desconectado; la base de datos conserva los datos y al reconectar el cliente vuelve a consultar la API REST.

## 4. Consistencia eventual

Los clientes pueden quedar momentáneamente desactualizados durante un corte, pero convergen al estado persistido cuando vuelven a consultar la API. Los avisos aceleran la actualización; no reemplazan la fuente de verdad.

## 5. Redis pub/sub, RabbitMQ y Kafka

Redis pub/sub es liviano y útil para avisos en vivo, pero no conserva los mensajes para clientes desconectados. RabbitMQ ofrece colas y confirmaciones para distribuir tareas entre consumidores. Kafka conserva un registro ordenado de eventos durante un período y sirve para alto volumen, reprocesamiento y analítica. Para TaskFlow, Redis Channels alcanza porque el cliente puede recuperar el estado por REST.

## 6. Escalado vertical y horizontal

El escalado vertical aumenta recursos de una máquina; el horizontal agrega instancias. Un layer en memoria pertenece a un solo proceso: si una conexión está en la instancia A y la API publica desde B, B no conoce el grupo. Redis permite compartir grupos entre procesos.

## 7. Publicar después de confirmar

Si una transacción se revierte después de emitir el evento, los clientes verían un cambio que nunca quedó guardado. Por eso el aviso se publica luego de guardar o con `transaction.on_commit` cuando hay una transacción.

## 8. CORS y Cross-Site WebSocket Hijacking

CORS regula solicitudes HTTP del navegador y no protege el handshake WebSocket. Con autenticación basada solo en cookies, un sitio malicioso podría intentar abrir una conexión usando la sesión del navegador. TaskFlow exige un access JWT explícito en la URL y valida membresía antes de aceptar; no alcanza con una cookie.

## 9. Casos difíciles de presencia

Varias pestañas: cerrar una no debería marcar offline mientras otra siga conectada; se resuelve contando conexiones por usuario y avisando offline al llegar a cero. Cortes de red sin cierre limpio: se detectan con heartbeats y vencimiento por timeout.

## 10. Reconexión

Backoff aumenta la espera entre intentos fallidos; jitter suma variación aleatoria para repartir los reintentos; resincronización consulta la API REST al abrir de nuevo para recuperar eventos perdidos.

## Tarea: eventos adicionales

TaskFlow emite `task_updated` al editar y `task_completed` al completar. Ambos pasan por `NotificationService._send`, que publica en el grupo del proyecto y registra el fallo sin deshacer el guardado si Redis no está disponible.
