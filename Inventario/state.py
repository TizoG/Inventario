"""
Estado de Reflex para gestionar datos de la base de datos
"""

import reflex as rx
from .database import db
from typing import List, Dict, Any


class InventarioState(rx.State):
    """Estado global para el inventario"""
    
    # Productos
    productos: List[Dict[str, Any]] = []
    producto_seleccionado: Dict[str, Any] = {}
    
    # Movimientos
    movimientos: List[Dict[str, Any]] = []
    
    # Estadísticas
    total_productos: int = 0
    cantidad_total: int = 0
    valor_total: float = 0
    
    # Form fields
    form_nombre: str = ""
    form_descripcion: str = ""
    form_cantidad: str = "0"
    form_precio: str = "0"
    form_categoria: str = ""
    form_unidad: str = ""
    form_proveedor: str = ""
    form_estado: str = ""
    form_stock_minimo: str = "0"
    # Form errors
    form_error: str = ""
    form_errors: dict = {}
    # UI state
    show_add_modal: bool = False
    show_view_modal: bool = False
    show_edit_modal: bool = False
    producto_seleccionado: Dict[str, Any] = {}

    # Filters
    search_query: str = ""
    filter_categoria: str = ""
    filter_estado: str = ""
    productos_display: List[Dict[str, Any]] = []
    
    # Métodos para cargar datos
    def cargar_productos(self):
        """Carga todos los productos desde la BD"""
        self.productos = db.obtener_productos()
        self.productos_display = list(self.productos)
    
    def cargar_movimientos(self):
        """Carga todos los movimientos desde la BD"""
        self.movimientos = db.obtener_movimientos()
    
    def cargar_estadisticas(self):
        """Carga estadísticas de la BD"""
        stats = db.obtener_estadisticas()
        self.total_productos = stats['total_productos']
        self.cantidad_total = stats['cantidad_total']
        self.valor_total = stats['valor_total']
    
    def cargar_todo(self):
        """Carga productos, movimientos y estadísticas"""
        self.cargar_productos()
        self.cargar_movimientos()
        self.cargar_estadisticas()
        self.aplicar_filtros()
    
    # Métodos para productos
    def agregar_producto(self):
        """Agrega un nuevo producto desde el formulario"""
        # Validación básica por campos
        if not self.validar_formulario():
            rx.toast("Corrige los errores del formulario")
            return
        
        try:
            cantidad = int(self.form_cantidad) if self.form_cantidad else 0
            precio = float(self.form_precio) if self.form_precio else 0
            
            db.agregar_producto(
                nombre=self.form_nombre,
                cantidad=cantidad,
                precio_unitario=precio,
                descripcion=self.form_descripcion,
                categoria=self.form_categoria,
                unidad_medida=self.form_unidad,
                proveedor=self.form_proveedor,
                estado=self.form_estado,
                stock_minimo=int(self.form_stock_minimo) if self.form_stock_minimo else 0,
            )
            
            # Limpiar formulario
            self.form_nombre = ""
            self.form_descripcion = ""
            self.form_cantidad = "0"
            self.form_precio = "0"
            self.form_categoria = ""
            self.form_unidad = ""
            self.form_proveedor = ""
            self.form_estado = ""
            self.form_stock_minimo = "0"
            self.form_error = ""
            
            # Recargar productos
            self.cargar_todo()
            rx.toast("Producto agregado exitosamente")
            self.close_add_modal()
        
        except Exception as e:
            self.form_error = str(e)
            rx.toast(f"Error: {str(e)}")

    def open_add_modal(self):
        self.show_add_modal = True

    def close_add_modal(self):
        self.show_add_modal = False

    def open_view_modal(self, producto: Dict[str, Any]):
        self.producto_seleccionado = producto
        self.show_view_modal = True

    def close_view_modal(self):
        self.show_view_modal = False

    def open_edit_modal(self, producto: Dict[str, Any]):
        # Prefill form with producto data
        self.producto_seleccionado = producto
        self.form_nombre = producto.get('nombre', '')
        self.form_descripcion = producto.get('descripcion', '')
        self.form_cantidad = str(producto.get('cantidad', 0))
        self.form_precio = str(producto.get('precio_unitario', 0))
        self.form_categoria = producto.get('categoria', '')
        self.form_unidad = producto.get('unidad_medida', '')
        self.form_proveedor = producto.get('proveedor', '')
        self.form_estado = producto.get('estado', '')
        self.form_stock_minimo = str(producto.get('stock_minimo', 0))
        self.show_edit_modal = True

    def close_edit_modal(self):
        self.show_edit_modal = False

    def aplicar_filtros(self):
        q = (self.search_query or "").strip().lower()
        cat = (self.filter_categoria or "").lower()
        est = (self.filter_estado or "").lower()

        def match(p):
            if q:
                if q not in str(p.get('nombre','')).lower() and q not in str(p.get('proveedor','')).lower():
                    return False
            if cat and cat != 'all' and cat != str(p.get('categoria','')).lower():
                return False
            if est and est != 'all' and est != str(p.get('estado','')).lower():
                return False
            return True

        self.productos_display = [p for p in self.productos if match(p)]

    def actualizar_producto(self, producto_id: int):
        # Validar antes de actualizar
        if not self.validar_formulario():
            rx.toast('Corrige los errores del formulario')
            return
        try:
            campos = {
                'nombre': self.form_nombre,
                'descripcion': self.form_descripcion,
                'cantidad': int(self.form_cantidad) if self.form_cantidad else 0,
                'precio_unitario': float(self.form_precio) if self.form_precio else 0,
                'categoria': self.form_categoria,
                'unidad_medida': self.form_unidad,
                'proveedor': self.form_proveedor,
                'estado': self.form_estado,
                'stock_minimo': int(self.form_stock_minimo) if self.form_stock_minimo else 0,
            }
            ok = db.actualizar_producto(producto_id, **campos)
            if ok:
                self.cargar_todo()
                self.close_edit_modal()
                rx.toast('Producto actualizado')
            else:
                rx.toast('No se pudo actualizar')
        except Exception as e:
            rx.toast(f'Error: {e}')

    def validar_formulario(self) -> bool:
        """Valida campos del formulario y llena `form_errors` con mensajes por campo."""
        errors = {}
        if not self.form_nombre or not self.form_nombre.strip():
            errors['nombre'] = 'Nombre requerido'
        try:
            cantidad = int(self.form_cantidad)
            if cantidad < 0:
                errors['cantidad'] = 'Cantidad debe ser >= 0'
        except Exception:
            errors['cantidad'] = 'Cantidad inválida'
        try:
            precio = float(self.form_precio)
            if precio < 0:
                errors['precio'] = 'Precio debe ser >= 0'
        except Exception:
            errors['precio'] = 'Precio inválido'
        if not self.form_categoria or not self.form_categoria.strip():
            errors['categoria'] = 'Categoría requerida'
        if not self.form_unidad or not self.form_unidad.strip():
            errors['unidad'] = 'Unidad de medida requerida'
        if not self.form_proveedor or not self.form_proveedor.strip():
            errors['proveedor'] = 'Proveedor requerido'
        if not self.form_estado or not self.form_estado.strip():
            errors['estado'] = 'Estado requerido'
        try:
            stock = int(self.form_stock_minimo)
            if stock < 0:
                errors['stock'] = 'Stock mínimo inválido'
        except Exception:
            errors['stock'] = 'Stock mínimo inválido'

        self.form_errors = errors
        return len(errors) == 0
    
    def eliminar_producto(self, producto_id: int):
        """Elimina un producto"""
        try:
            db.eliminar_producto(producto_id)
            self.cargar_todo()
            rx.toast("Producto eliminado")
        except Exception as e:
            rx.toast(f"Error: {str(e)}")
    
    # Métodos para movimientos
    def registrar_entrada(self, producto_id: int, cantidad: int, motivo: str = ""):
        """Registra una entrada de inventario"""
        try:
            db.registrar_movimiento(producto_id, 'entrada', cantidad, motivo)
            self.cargar_todo()
            rx.toast("Entrada registrada")
        except Exception as e:
            rx.toast(f"Error: {str(e)}")
    
    def registrar_salida(self, producto_id: int, cantidad: int, motivo: str = ""):
        """Registra una salida de inventario"""
        try:
            db.registrar_movimiento(producto_id, 'salida', cantidad, motivo)
            self.cargar_todo()
            rx.toast("Salida registrada")
        except Exception as e:
            rx.toast(f"Error: {str(e)}")
    
    # Métodos auxiliares
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.form_nombre = ""
        self.form_descripcion = ""
        self.form_cantidad = "0"
        self.form_precio = "0"
        self.form_categoria = ""
