import json
from pathlib import Path


def validar_datos(nombre_archivo):
    """Valida un JSON de productos; devuelve la lista o None si hay errores."""
    archivo = Path(nombre_archivo)
    try:
        with archivo.open(mode="r", encoding="utf-8") as archivo_json:
            datos = json.load(archivo_json)

        if not isinstance(datos, list):
            raise ValueError("El archivo no contiene una lista de productos.")

        for indice, producto in enumerate(datos, start=1):
            if not isinstance(producto, dict):
                raise ValueError(f"El elemento {indice} no es un objeto de producto.")
            precio = producto.get("precio")
            if isinstance(precio, bool) or not isinstance(precio, (int, float)):
                nombre = producto.get("nombre", f"fila {indice}")
                raise TypeError(f"El precio de '{nombre}' no es numérico.")

        print("Validación exitosa.")
        return datos

    except FileNotFoundError:
        print(f"Error: el archivo '{archivo.name}' no se encontró.")
    except json.JSONDecodeError as error:
        print(f"Error: el archivo no tiene un formato JSON válido ({error}).")
    except (ValueError, TypeError) as error:
        print(f"Error en la validación de datos: {error}")
    return None
