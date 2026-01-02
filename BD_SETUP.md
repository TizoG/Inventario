# 📦 Guía de Base de Datos Local - Sistema de Inventario

## 🚀 Configuración Inicial

### 1. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 2. **Agregar datos de ejemplo (opcional)**
```bash
python agregar_datos_ejemplo.py
```

Esto creará la BD automáticamente en `data/inventario.db` y agregará 5 productos de ejemplo.

---

## 📋 Estructura de la Base de Datos

### Tabla: `productos`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único (auto-incrementado) |
| nombre | TEXT | Nombre del producto |
| descripcion | TEXT | Descripción opcional |
| cantidad | INTEGER | Cantidad en stock |
| precio_unitario | REAL | Precio por unidad |
| categoria | TEXT | Categoría del producto |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| fecha_actualizacion | TIMESTAMP | Fecha de última actualización |

### Tabla: `movimientos`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| producto_id | INTEGER | ID del producto (FK) |
| tipo | TEXT | 'entrada' o 'salida' |
| cantidad | INTEGER | Cantidad movida |
| motivo | TEXT | Motivo del movimiento |
| fecha | TIMESTAMP | Fecha del movimiento |

---

## 💻 Uso en tu aplicación

### **Importar el módulo de BD**
```python
from Inventario.database import db

# Agregar un producto
db.agregar_producto(
    nombre="Laptop",
    cantidad=10,
    precio_unitario=999.99,
    descripcion="Laptop Gaming",
    categoria="Electrónica"
)

# Obtener todos los productos
productos = db.obtener_productos()

# Registrar movimiento
db.registrar_movimiento(producto_id=1, tipo='entrada', cantidad=5, motivo='Reabastecimiento')

# Obtener estadísticas
stats = db.obtener_estadisticas()
```

---

## 🎯 Métodos disponibles en `database.py`

### Productos
- `agregar_producto(nombre, cantidad, precio_unitario, descripcion, categoria)` - Agrega un producto
- `obtener_productos()` - Obtiene todos los productos
- `obtener_producto(producto_id)` - Obtiene un producto específico
- `actualizar_producto(producto_id, **kwargs)` - Actualiza campos
- `eliminar_producto(producto_id)` - Elimina un producto

### Movimientos
- `registrar_movimiento(producto_id, tipo, cantidad, motivo)` - Registra entrada/salida
- `obtener_movimientos(producto_id=None)` - Obtiene historial

### Estadísticas
- `obtener_estadisticas()` - Total productos, cantidad y valor

---

## 🔧 Estado en Reflex (`state.py`)

El estado `InventarioState` proporciona:
- `cargar_productos()` - Carga productos desde la BD
- `cargar_movimientos()` - Carga movimientos
- `cargar_estadisticas()` - Carga estadísticas
- `cargar_todo()` - Carga todo
- `agregar_producto()` - Agrega desde formulario
- `eliminar_producto(id)` - Elimina producto
- `registrar_entrada(id, cantidad, motivo)` - Entrada de inventario
- `registrar_salida(id, cantidad, motivo)` - Salida de inventario

---

## 📍 Acceder a la página de inventario

Una vez que la app esté corriendo:
```
http://localhost:3000/inventario
```

---

## ✅ Próximos pasos

1. Personaliza los campos según tus necesidades
2. Agrega más validaciones
3. Crea reportes
4. Integra con tu sistema de ventas
