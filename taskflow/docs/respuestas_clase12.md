# Clase 12 — Preguntas de repaso

## 1. Pirámide de tests

En la base hay muchos unitarios: `TaskService.mark_completed`. En el medio, integración: POST de tareas con permisos y base. En la punta, pocos E2E con navegador y servidor completo. Son pocos porque tardan más y se rompen con cambios de interfaz.

## 2. AAA y FIRST

AAA: preparar datos (Arrange), ejecutar (Act) y verificar (Assert). FIRST: rápidos, independientes, repetibles, auto-verificables y escritos a tiempo junto al código.

## 3. Stub, mock y fake

Un stub da una respuesta fija (feriados de prueba). Un mock, además, permite comprobar cómo lo llamaron. Un fake funciona de manera simple pero real, como `InMemoryChannelLayer` durante los tests.

## 4. Aislamiento

pytest-django prepara una base de prueba separada y revierte los cambios de cada test; las fixtures recrean los datos necesarios para cada caso.

## 5. Cobertura

La cobertura de líneas mide qué instrucciones se ejecutaron. La de ramas comprueba además los dos caminos de decisiones como `if/else`.

## 6. Prácticas de integración continua

Integrar cambios pequeños y frecuentes, mantener `main` verde, y hacer pasar cada pull request por el pipeline antes de fusionarlo.

## 7. Entrega y despliegue continuos

Entrega continua automatiza hasta dejar una versión lista, pero una persona decide publicarla. Despliegue continuo publica automáticamente cada cambio que supera los controles.

## 8. Términos de GitHub Actions

Workflow: proceso definido en YAML. Job: grupo de pasos. Step: comando o acción ejecutada. Runner: máquina que ejecuta el job. Action: paso reutilizable, como `actions/checkout`.

## 9. Contenedores y máquinas virtuales

Una máquina virtual incluye un sistema operativo completo y comparte menos recursos; un contenedor empaqueta la aplicación y comparte el kernel del host. Una imagen es una plantilla de solo lectura, un contenedor es una imagen en ejecución y un registro almacena/publica imágenes.

## 10. Paridad de ambientes

Paridad significa que desarrollo y producción usan configuraciones y servicios parecidos, con secretos propios por ambiente. Compose levanta localmente la aplicación, PostgreSQL y Redis con la misma topología de producción.

## 11. Observabilidad

Logs registran eventos, métricas agregan cantidades y tiempos, y trazas siguen una petición a través de servicios.

## 12. SemVer

Parche: arreglar un bug sin cambiar contratos (`1.0.0` a `1.0.1`). Menor: añadir un endpoint compatible (`1.0.1` a `1.1.0`). Mayor: quitar un campo de respuesta (`1.1.0` a `2.0.0`).

## 13. Estrategias de despliegue y migraciones

Rolling actualiza instancias de a una. Blue-green levanta la versión nueva en paralelo y cambia el tráfico de golpe. Canary expone primero una fracción de usuarios. Las migraciones pueden cambiar o transformar datos; volver atrás el código no revierte automáticamente esos cambios, por eso se preparan pasos compatibles con versiones anteriores.
