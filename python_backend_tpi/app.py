import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_CSV = BASE_DIR / "datos.csv"
ARCHIVO_JSON = BASE_DIR / "salida.json"
PRODUCTOS = [
    {"nombre": "Laptop", "precio": 1200, "stock": 15},
    {"nombre": "Mouse", "precio": 25, "stock": 5},
    {"nombre": "Teclado", "precio": 75, "stock": 25},
    {"nombre": "Monitor", "precio": 300, "stock": 8},
]


def calcular_promedio_precio(productos):
    if not productos:
        return 0
    return sum(producto["precio"] for producto in productos) / len(productos)


def cargar_productos_csv(ruta):
    productos = []
    with ruta.open(mode="r", encoding="utf-8", newline="") as archivo:
        for fila in csv.DictReader(archivo):
            fila["id"] = int(fila["id"])
            fila["precio"] = int(fila["precio"])
            fila["stock"] = int(fila["stock"])
            productos.append(fila)
    return productos


def main():
    bajo_stock = [producto for producto in PRODUCTOS if producto["stock"] < 10]
    print("Productos con bajo stock:", bajo_stock)
    print(f"Precio promedio: ${calcular_promedio_precio(PRODUCTOS):.2f}")

    productos_csv = cargar_productos_csv(ARCHIVO_CSV)
    print("Productos cargados desde CSV:", productos_csv)
    ARCHIVO_JSON.write_text(
        json.dumps(productos_csv, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Archivo {ARCHIVO_JSON.name} creado.")


if __name__ == "__main__":
    main()
