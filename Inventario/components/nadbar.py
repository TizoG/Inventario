import reflex as rx

from .icon_button import icon_button

def nadbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.flex(
                rx.icon("box",size=35),
                rx.text("Gestion de Inventario", size="5"),
                spacing="3",
                align="center",
            ),
            rx.hstack(
                icon_button(
                "home",
                "/"
                ),
                icon_button(
                "box",
                "/"
                ),
                icon_button(
                "search",
                "/"
                ),
                icon_button(
                "folder",
                "/"
                ),
                icon_button(
                "settings",
                "/"
                ),
                icon_button(
                "user",
                "/"
                ),
                spacing="5"
            ),
            
            justify="between"
        ),
        padding_x="2rem",
        padding_y="2rem",
        bg="#1D3557",
        color="white"

    )