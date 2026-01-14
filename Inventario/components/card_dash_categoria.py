import reflex as rx
from ..state import InventarioState

def card_dash_categoria()->rx.Component:
    return rx.box(
        rx.card(
            rx.vstack(
                rx.text(
                    "Distribuicion por categorias",
                    color="#1D3557"
                ),
                rx.text(
                    "Cantidad de materiales por categoría",
                    color="#1D3557"
                ),
                rx.divider(),
                rx.foreach(
                    InventarioState.categorias,
                    lambda item: rx.hstack(
                        rx.text(
                            item["categoria"] ,
                            width="60%",
                            color="#1D3557"
                        ),
                        rx.text(
                            f'{item["cantidad_total"]}',
                            font_weight="bold",
                            color="#2A9D8F"
                        ),
                        justify="between",
                        width="100%"
                    )
                )
            )
        ),
        width="100%"
    )