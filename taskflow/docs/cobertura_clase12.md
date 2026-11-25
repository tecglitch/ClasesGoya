# Reporte de cobertura — Clase 12

Comando ejecutado en el entorno virtual de `ClasesGoya`:

```text
pytest -v --cov=core --cov-report=term-missing
```

**Resultado:** 9 pruebas aprobadas, 0 fallidas. Cobertura global de `core`: **62%** de líneas.

Las pruebas cubren servicios de tareas y feriados, autenticación y permisos de endpoints REST, aislamiento de datos por proyecto, y autenticación, consultas y mutations GraphQL. La cobertura aún es parcial: quedan por probar con más detalle los consumers WebSocket, los permisos y acciones administrativas, el importador de datos y rutas de error. Una línea ejecutada no prueba por sí sola que su comportamiento sea correcto; el reporte debe orientar nuevas pruebas.
