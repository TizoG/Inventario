"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from .pages.home import home
from .pages.inventario import inventario
from .state import InventarioState
from .components.nadbar import nadbar

from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    return rx.box(
        home(),
        
    )


def inventario_page() -> rx.Component:
    """Página de inventario con carga de datos"""
    return rx.vstack(
        nadbar(),
        inventario(),
        on_mount=InventarioState.cargar_todo,
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",      # Esto fuerza el modo claro
        has_background=True,     # Asegura que el fondo respete el tema
        accent_color="blue",     # Opcional: tu color de acento
    )
)
app.add_page(index, route="/")
app.add_page(inventario_page, route="/inventario")
