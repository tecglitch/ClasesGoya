# Preparación del entorno — Clase 1, Parte 1

Este directorio contiene el ejercicio de Python del curso.

## Requisitos

- Python 3.10 o superior.
- Visual Studio Code (opcional).

## Crear el entorno virtual

Desde esta carpeta, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

El ejercicio utiliza la biblioteca estándar de Python y no necesita instalar paquetes externos.

## Ejercicio de Python

Se recorren productos con `for`, se filtran los de bajo stock y se calcula el precio promedio. Ejecutar con:

```powershell
python app.py
```
