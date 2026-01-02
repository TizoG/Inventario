"""
Script para llenar la base de datos con datos de ejemplo
Ejecuta este script una sola vez para agregar datos iniciales
"""

from Inventario.database import db


def agregar_datos_ejemplo():
    """Agrega datos de ejemplo a la base de datos"""
    
    productos_ejemplo = [
        {
            "nombre": "Laptop Dell",
            "cantidad": 5,
            "precio_unitario": 899.99,
            "descripcion": "Laptop Dell XPS 15",
            "categoria": "Electrónica"
        },
        {
            "nombre": "Mouse Logitech",
            "cantidad": 25,
            "precio_unitario": 29.99,
            "descripcion": "Mouse inalámbrico",
            "categoria": "Accesorios"
        },
        {
            "nombre": "Teclado Mecánico",
            "cantidad": 12,
            "precio_unitario": 149.99,
            "descripcion": "Teclado RGB",
            "categoria": "Accesorios"
        },
        {
            "nombre": "Monitor LG 27",
            "cantidad": 8,
            "precio_unitario": 299.99,
            "descripcion": "Monitor 4K UltraWide",
            "categoria": "Pantallas"
        },
        {
            "nombre": "Cable USB-C",
            "cantidad": 50,
            "precio_unitario": 12.99,
            "descripcion": "Cable de carga y datos",
            "categoria": "Cables"
        },
    ]
    
    for producto in productos_ejemplo:
        db.agregar_producto(**producto)
    
    print(f"✅ {len(productos_ejemplo)} productos agregados a la BD")
    
    # Registrar algunos movimientos de ejemplo
    db.registrar_movimiento(1, 'entrada', 3, 'Compra inicial')
    db.registrar_movimiento(1, 'salida', 1, 'Venta')
    db.registrar_movimiento(2, 'entrada', 10, 'Reabastecimiento')
    
    print("✅ Movimientos de inventario registrados")
    
    # Mostrar estadísticas
    stats = db.obtener_estadisticas()
    print("\n📊 Estadísticas:")
    print(f"  Total productos: {stats['total_productos']}")
    print(f"  Cantidad total: {stats['cantidad_total']}")
    print(f"  Valor total: ${stats['valor_total']:.2f}")


if __name__ == "__main__":
    agregar_datos_ejemplo()
