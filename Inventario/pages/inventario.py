"""
Página de gestión de inventario
"""

import reflex as rx
from ..state import InventarioState


def formulario_producto() -> rx.Component:
    """Formulario para agregar productos"""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.text("Agregar Producto", color="white", font_weight="bold"),
                padding="0.75rem",
                bg="#457B9D",
                width="100%",
                border_radius="6px 6px 0 0",
            ),
            rx.vstack(
                        rx.input(
                            placeholder="Nombre del producto",
                            value=InventarioState.form_nombre,
                            on_change=InventarioState.set_form_nombre,
                            width="100%",
                            bg="#f8fafc",
                            border_radius="6px",
                            padding="0.5rem",
                        ),
                rx.input(
                    placeholder="Descripción",
                    value=InventarioState.form_descripcion,
                    on_change=InventarioState.set_form_descripcion,
                    width="100%",
                    bg="#f8fafc",
                    border_radius="6px",
                    padding="0.5rem",
                ),
                        rx.hstack(
                            rx.input(
                                placeholder="Unidad de medida",
                                value=InventarioState.form_unidad,
                                on_change=InventarioState.set_form_unidad,
                                width="50%",
                            ),
                            rx.input(
                                placeholder="Proveedor",
                                value=InventarioState.form_proveedor,
                                on_change=InventarioState.set_form_proveedor,
                                width="50%",
                            ),
                            spacing="3",
                        ),
                        rx.hstack(
                            rx.input(
                                placeholder="Estado (ej. disponible)",
                                value=InventarioState.form_estado,
                                on_change=InventarioState.set_form_estado,
                                width="50%",
                            ),
                            rx.input(
                                placeholder="Stock mínimo",
                                value=InventarioState.form_stock_minimo,
                                on_change=InventarioState.set_form_stock_minimo,
                                type_="number",
                                width="50%",
                            ),
                            spacing="3",
                        ),
            rx.input(
                placeholder="Cantidad",
                value=InventarioState.form_cantidad,
                on_change=InventarioState.set_form_cantidad,
                type_="number",
                width="100%",
            ),
            rx.input(
                placeholder="Precio unitario",
                value=InventarioState.form_precio,
                on_change=InventarioState.set_form_precio,
                type_="number",
                width="100%",
            ),
            rx.input(
                placeholder="Categoría",
                value=InventarioState.form_categoria,
                on_change=InventarioState.set_form_categoria,
                width="100%",
            ),
                rx.hstack(
                    rx.button(
                        "Agregar Producto",
                        on_click=InventarioState.agregar_producto,
                        color_scheme="blue",
                    ),
                    rx.button(
                        "Limpiar",
                        on_click=InventarioState.limpiar_formulario,
                        variant="outline",
                        color_scheme="gray",
                    ),
                    spacing="3",
                ),
                # Mensaje de error inline
                rx.cond(
                    InventarioState.form_error,
                    rx.text(InventarioState.form_error, color="red", font_size="sm"),
                ),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        max_width="720px",
        padding="0",
        border="1px solid #e2e8f0",
        border_radius="8px",
        box_shadow="sm",
        bg="white",
        color="black",
    )


def tabla_productos() -> rx.Component:
    """Lista de productos estilizada"""
    return rx.box(
        rx.vstack(
            rx.heading("Productos", size="3"),
            # filtros
            rx.hstack(
                rx.input(placeholder='Buscar por nombre o proveedor', value=InventarioState.search_query, on_change=InventarioState.set_search_query, width='50%'),
                rx.input(placeholder='Categoría', value=InventarioState.filter_categoria, on_change=InventarioState.set_filter_categoria, width='20%'),
                rx.input(placeholder='Estado', value=InventarioState.filter_estado, on_change=InventarioState.set_filter_estado, width='20%'),
                rx.button('Buscar', on_click=InventarioState.aplicar_filtros, color_scheme='blue'),
                spacing='3',
                width='100%'
            ),
                rx.cond(
                InventarioState.productos_display,
                rx.grid(
                    rx.foreach(
                        InventarioState.productos_display,
                        lambda producto: rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text(producto['nombre'], font_weight='bold'),
                                    rx.text(producto.get('estado',''), font_weight='bold'),
                                    width='100%',
                                    justify='between'
                                ),
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(f"Unidades: {producto.get('cantidad',0)}"),
                                        rx.text(f"Proveedor: {producto.get('proveedor','-')}")
                                    ),
                                    rx.vstack(
                                        rx.text(f"Categoría: {producto.get('categoria','-')}") ,
                                        rx.text(f"Creado: {producto.get('fecha_creacion','-')}")
                                    ),
                                    spacing='4',
                                    width='100%'
                                ),
                                rx.hstack(
                                    rx.button('Ver', on_click=lambda producto=producto: InventarioState.open_view_modal(producto), color_scheme='blue'),
                                    rx.button('Editar', on_click=lambda producto=producto: InventarioState.open_edit_modal(producto), variant='outline', color_scheme='gray'),
                                    rx.icon_button('trash', on_click=lambda producto=producto: InventarioState.eliminar_producto(producto['id']), color='red'),
                                    spacing='3'
                                ),
                                spacing='3'
                            ),
                            padding='1rem',
                            border_radius='8px',
                            box_shadow='sm',
                            bg=rx.cond(
                                producto['categoria'] == 'material',
                                'linear-gradient(90deg, #457B9D, #1D3557)',
                                rx.cond(
                                    producto['categoria'] == 'herramienta',
                                    'linear-gradient(90deg, #22C55E, #15803D)',
                                    rx.cond(
                                        producto['categoria'] == 'quimico',
                                        'linear-gradient(90deg, #EAB308, #A16207)',
                                        'linear-gradient(90deg, #667eea, #764ba2)'
                                    ),
                                ),
                            ),
                        ),
                    ),
                    columns='3',
                    gap='1rem'
                ),
                rx.text("No hay productos", color="gray"),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        padding="1rem",
        border="1px solid #e2e8f0",
        border_radius="8px",
        box_shadow="sm",
        bg="white",
        color="black",
    )


def estadisticas() -> rx.Component:
    """Tarjetas de estadísticas"""
    return rx.hstack(
        rx.card(
            rx.vstack(
                rx.text("Total de Productos", font_weight="bold"),
                rx.text(InventarioState.total_productos, font_size="2xl"),
                spacing="2",
                align="center",
            ),
            width="100%",
            padding="1rem",
        ),
        rx.card(
            rx.vstack(
                rx.text("Cantidad Total", font_weight="bold"),
                rx.text(InventarioState.cantidad_total, font_size="2xl"),
                spacing="2",
                align="center",
            ),
            width="100%",
            padding="1rem",
        ),
        rx.card(
            rx.vstack(
                rx.text("Valor Total", font_weight="bold"),
                rx.text(f"${InventarioState.valor_total:.2f}", font_size="2xl"),
                spacing="2",
                align="center",
            ),
            width="100%",
            padding="1rem",
        ),
        width="100%",
        spacing="4",
    )


def inventario() -> rx.Component:
    """Página principal de inventario"""
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text("Panel de materiales", font_size="2xl", font_weight="bold"),
                rx.text("Gestiona tu inventario de materiales de forma eficiente", color="gray"),
            ),
            rx.spacer(),
            rx.button("Agregar material", on_click=lambda: InventarioState.set_show_add_modal(True), color_scheme="blue"),
            width="100%",
            align="center",
        ),
        # Indicador temporal para depuración: muestra si el modal está abierto
        rx.cond(
            InventarioState.show_add_modal,
            rx.text("MODAL ABIERTO", color="green", font_weight="bold"),
            rx.text("MODAL CERRADO", color="gray"),
        ),
        # Overlay para agregar producto (compatible, centrado y proporcional)
        rx.cond(
            InventarioState.show_add_modal,
            rx.box(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text('Nuevo material', font_weight='bold', font_size='lg'),
                            rx.button('Cancelar', on_click=InventarioState.close_add_modal, variant='ghost'),
                            width='100%',
                            justify='between'
                        ),
                        formulario_producto(),
                    ),
                    padding="1rem",
                    width='clamp(320px,90%,720px)',
                    border_radius='8px',
                    bg='white',
                    role='dialog',
                    aria_label='Agregar producto',
                ),
                position="fixed",
                inset="0",
                display='flex',
                align_items="center",
                justify_content="center",
                bg="rgba(0,0,0,0.4)",
                padding="1.5rem",
                z_index=50,
            ),
        ),
        # Overlay para editar producto (compatible, centrado y proporcional)
        rx.cond(
            InventarioState.show_edit_modal,
            rx.box(
                rx.box(
                    rx.vstack(
                        rx.hstack(rx.text('Editar Producto', font_weight='bold'), rx.button('Cancelar', on_click=InventarioState.close_edit_modal, variant='ghost'), width='100%', justify='between'),
                        rx.vstack(
                            rx.input(placeholder='Nombre del producto', value=InventarioState.form_nombre, on_change=InventarioState.set_form_nombre, width='100%'),
                            rx.cond(InventarioState.form_errors.get('nombre'), rx.text(InventarioState.form_errors.get('nombre'), color='red', font_size='sm')),
                            rx.input(placeholder='Descripción', value=InventarioState.form_descripcion, on_change=InventarioState.set_form_descripcion, width='100%'),
                            rx.hstack(rx.input(placeholder='Unidad de medida', value=InventarioState.form_unidad, on_change=InventarioState.set_form_unidad, width='50%'), rx.input(placeholder='Proveedor', value=InventarioState.form_proveedor, on_change=InventarioState.set_form_proveedor, width='50%'), spacing='3'),
                            rx.hstack(rx.input(placeholder='Estado', value=InventarioState.form_estado, on_change=InventarioState.set_form_estado, width='50%'), rx.input(placeholder='Stock mínimo', value=InventarioState.form_stock_minimo, on_change=InventarioState.set_form_stock_minimo, width='50%'), spacing='3'),
                            rx.input(placeholder='Cantidad', value=InventarioState.form_cantidad, on_change=InventarioState.set_form_cantidad, type_='number', width='100%'),
                            rx.cond(InventarioState.form_errors.get('cantidad'), rx.text(InventarioState.form_errors.get('cantidad'), color='red', font_size='sm')),
                            rx.input(placeholder='Precio unitario', value=InventarioState.form_precio, on_change=InventarioState.set_form_precio, type_='number', width='100%'),
                            rx.cond(InventarioState.form_errors.get('precio'), rx.text(InventarioState.form_errors.get('precio'), color='red', font_size='sm')),
                            rx.hstack(rx.button('Guardar cambios', on_click=lambda: InventarioState.actualizar_producto(InventarioState.producto_seleccionado.get('id')), color_scheme='blue'), rx.button('Cancelar', on_click=InventarioState.close_edit_modal, variant='outline'), spacing='3'),
                        ),
                    ),
                    padding='1rem',
                    width='clamp(320px,90%,720px)',
                    border_radius='8px',
                    bg='white',
                    role='dialog',
                    aria_label='Editar producto',
                ),
                position='fixed',
                inset='0',
                display='flex',
                align_items='center',
                justify_content='center',
                bg='rgba(0,0,0,0.4)',
                padding='1.5rem',
                z_index=50,
            ),
        ),
        estadisticas(),
        # Mostrar tabla principal; el formulario solo aparece en el modal
        rx.hstack(
            rx.box(
                tabla_productos(),
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        spacing="6",
        padding_x="2rem",
        padding_y="1.5rem",
        width="100%",
    )
