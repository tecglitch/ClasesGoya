# Clase 1 - Python, CSV, JSON y validación modular

## Qué se completó

- Preparación del proyecto y entorno virtual Python.
- Lista de productos, recorrido con `for`, filtro de stock menor a 10 y promedio de precios.
- Lectura de `datos.csv` con `csv.DictReader`, `with` y conversión de campos numéricos.
- Conversión de CSV a JSON en `salida.json`.
- Validación de JSON y de precios numéricos en `validar_productos.py`.
- Demostración de un dato inválido en `salida_corrupta.json`; la salida correcta se conserva en `salida.json`.
- Modularización pedida en la Parte 4: `validar_datos()` devuelve los datos válidos o `None`.

## Requisitos del entorno

Python 3.10 o superior (la consigna de la Parte 1 admite 3.9+; el compendio recomienda 3.10+). VS Code está instalado. El editor de código puede elegirse según las preferencias de cada persona.

## Crear y activar el entorno virtual en Windows PowerShell

Desde esta carpeta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

En CMD, activarlo con `.venv\Scripts\activate.bat`. El ejercicio solo usa módulos de la biblioteca estándar, por lo que no requiere `pip install`.

## Ejecutar

```powershell
python app.py
```

La ejecución vuelve a generar `salida.json` (válido) y `salida_corrupta.json` (fixture para practicar el manejo de errores). La validación del archivo correcto imprime `Validación exitosa`; la del archivo corrupto explica el error y retorna `None`.

## Estructura

- `app.py`: datos en memoria, CSV, promedio y conversión a JSON.
- `validar_productos.py`: validador modular.
- `datos.csv`: datos de entrada.
- `salida.json`: datos válidos de salida.
- `salida_corrupta.json`: demostración de precio no numérico.

