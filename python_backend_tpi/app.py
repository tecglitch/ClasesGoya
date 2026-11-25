from pathlib import Path

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


def main():
    print("Productos:")
    for producto in PRODUCTOS:
        print(f"{producto['nombre']}: ${producto['precio']}")

    bajo_stock = [producto for producto in PRODUCTOS if producto["stock"] < 10]
    print("Productos con bajo stock:", bajo_stock)
    print(f"Precio promedio: ${calcular_promedio_precio(PRODUCTOS):.2f}")


if __name__ == "__main__":
    main()
