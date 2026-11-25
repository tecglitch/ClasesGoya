import csv
import json
from pathlib import Path

from validar_productos import validar_datos

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_CSV = BASE_DIR / "datos.csv"
ARCHIVO_JSON = BASE_DIR / "salida.json"
ARCHIVO_CORRUPTO = BASE_DIR / "salida_corrupta.json"


def calcular_promedio_precio(lista):
    """Devuelve el precio promedio, o 0 si la lista está vacía."""
    if not lista:
        return 0
    return sum(producto["precio"] for producto in lista) / len(lista)


def cargar_productos_csv(nombre_archivo):
    """Lee productos CSV y convierte sus campos numéricos a enteros."""
    productos = []
    with nombre_archivo.open(mode="r", encoding="utf-8", newline="") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for numero_fila, fila in enumerate(lector, start=2):
            try:
                fila["id"] = int(fila["id"])
                fila["precio"] = int(fila["precio"])
                fila["stock"] = int(fila["stock"])
            except (TypeError, ValueError, KeyError) as error:
                raise ValueError(f"Datos inválidos en la fila {numero_fila}: {error}") from error
            productos.append(fila)
    return productos


def main():
    productos = [
        {"nombre": "Laptop", "precio": 1200, "stock": 15},
        {"nombre": "Mouse", "precio": 25, "stock": 5},
        {"nombre": "Teclado", "precio": 75, "stock": 25},
        {"nombre": "Monitor", "precio": 300, "stock": 8},
    ]

    print("Productos en memoria:")
    productos_bajo_stock = []
    for producto in productos:
        print(f"Producto: {producto['nombre']}, Precio: ${producto['precio']}")
        if producto["stock"] < 10:
            productos_bajo_stock.append(producto)

    print("\nProductos con bajo stock:")
    print(productos_bajo_stock)
    print(f"\nPrecio promedio: ${calcular_promedio_precio(productos):.2f}")

    try:
        productos_desde_csv = cargar_productos_csv(ARCHIVO_CSV)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ARCHIVO_CSV.name}'.")
        return
    except ValueError as error:
        print(f"Error al leer el CSV: {error}")
        return

    print("\nProductos cargados desde CSV:")
    print(productos_desde_csv)

    ARCHIVO_JSON.write_text(
        json.dumps(productos_desde_csv, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nArchivo '{ARCHIVO_JSON.name}' creado con éxito.")

    print("\n--- Validación del archivo correcto ---")
    datos_validados = validar_datos(ARCHIVO_JSON)
    if datos_validados is not None:
        print(f"Datos validados correctamente: {len(datos_validados)} productos.")

    print("\n--- Demostración de un precio no numérico ---")
    corruptos = [dict(producto) for producto in productos_desde_csv]
    corruptos[0]["precio"] = "mil doscientos"
    ARCHIVO_CORRUPTO.write_text(
        json.dumps(corruptos, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    resultado_corrupto = validar_datos(ARCHIVO_CORRUPTO)
    print(f"El validador devolvió None: {resultado_corrupto is None}")


if __name__ == "__main__":
    main()
