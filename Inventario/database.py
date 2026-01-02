"""
Módulo de configuración y gestión de la base de datos SQLite
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

# Ruta de la BD local
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/inventario.db")

# Crear carpeta data si no existe
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


class Database:
    """Clase para gestionar operaciones con la base de datos"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
        return conn
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL DEFAULT 0,
                precio_unitario REAL NOT NULL,
                categoria TEXT,
                unidad_medida TEXT,
                proveedor TEXT,
                estado TEXT,
                stock_minimo INTEGER DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de movimientos de inventario (entrada/salida)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'salida')),
                cantidad INTEGER NOT NULL,
                motivo TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)
        
        conn.commit()
        conn.close()
        # Ensure new columns exist for schema updates
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(productos)")
        existing_cols = {row[1] for row in cursor.fetchall()}
        additional_cols = {
            'unidad_medida': "TEXT",
            'proveedor': "TEXT",
            'estado': "TEXT",
            'stock_minimo': "INTEGER DEFAULT 0",
        }
        for col, col_def in additional_cols.items():
            if col not in existing_cols:
                cursor.execute(f"ALTER TABLE productos ADD COLUMN {col} {col_def}")
        conn.commit()
        conn.close()
    
    # OPERACIONES CRUD PARA PRODUCTOS
    
    def agregar_producto(self, nombre: str, cantidad: int, precio_unitario: float, 
                        descripcion: str = "", categoria: str = "", unidad_medida: str = "", proveedor: str = "", estado: str = "", stock_minimo: int = 0) -> int:
        """Agrega un nuevo producto a la BD"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio_unitario, categoria, unidad_medida, proveedor, estado, stock_minimo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio_unitario, categoria, unidad_medida, proveedor, estado, stock_minimo))
        
        producto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return producto_id
    
    def obtener_productos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los productos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM productos ORDER BY fecha_creacion DESC")
        productos = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return productos
    
    def obtener_producto(self, producto_id: int) -> Dict[str, Any]:
        """Obtiene un producto específico por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def actualizar_producto(self, producto_id: int, **kwargs) -> bool:
        """Actualiza un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        campos_permitidos = ['nombre', 'descripcion', 'cantidad', 'precio_unitario', 'categoria', 'unidad_medida', 'proveedor', 'estado', 'stock_minimo']
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}
        
        if not campos:
            conn.close()
            return False
        
        campos['fecha_actualizacion'] = datetime.now()
        
        set_clause = ", ".join([f"{k} = ?" for k in campos.keys()])
        valores = list(campos.values()) + [producto_id]
        
        cursor.execute(f"UPDATE productos SET {set_clause} WHERE id = ?", valores)
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def eliminar_producto(self, producto_id: int) -> bool:
        """Elimina un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    # OPERACIONES PARA MOVIMIENTOS DE INVENTARIO
    
    def registrar_movimiento(self, producto_id: int, tipo: str, cantidad: int, motivo: str = "") -> int:
        """Registra una entrada o salida de inventario"""
        if tipo not in ['entrada', 'salida']:
            raise ValueError("El tipo debe ser 'entrada' o 'salida'")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Obtener producto actual
        cursor.execute("SELECT cantidad FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()
        
        if not producto:
            conn.close()
            raise ValueError(f"Producto con ID {producto_id} no existe")
        
        cantidad_actual = producto[0]
        
        # Validar que no haya cantidad negativa en salida
        if tipo == 'salida' and (cantidad_actual - cantidad) < 0:
            conn.close()
            raise ValueError("No hay suficiente inventario para esta salida")
        
        # Registrar movimiento
        cursor.execute("""
            INSERT INTO movimientos (producto_id, tipo, cantidad, motivo)
            VALUES (?, ?, ?, ?)
        """, (producto_id, tipo, cantidad, motivo))
        
        # Actualizar cantidad en productos
        nueva_cantidad = cantidad_actual + cantidad if tipo == 'entrada' else cantidad_actual - cantidad
        cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, producto_id))
        
        movimiento_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return movimiento_id
    
    def obtener_movimientos(self, producto_id: int = None) -> List[Dict[str, Any]]:
        """Obtiene los movimientos de inventario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if producto_id:
            cursor.execute("""
                SELECT m.*, p.nombre FROM movimientos m
                JOIN productos p ON m.producto_id = p.id
                WHERE m.producto_id = ?
                ORDER BY m.fecha DESC
            """, (producto_id,))
        else:
            cursor.execute("""
                SELECT m.*, p.nombre FROM movimientos m
                JOIN productos p ON m.producto_id = p.id
                ORDER BY m.fecha DESC
            """)
        
        movimientos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return movimientos
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del inventario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total_productos FROM productos")
        total_productos = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(cantidad) as cantidad_total FROM productos")
        cantidad_total = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(cantidad * precio_unitario) as valor_total FROM productos")
        valor_total = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_productos': total_productos,
            'cantidad_total': cantidad_total,
            'valor_total': valor_total
        }


# Instancia global de la base de datos
db = Database()
