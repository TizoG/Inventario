import reflex as rx

from ..components.nadbar import nadbar
from ..components.cards_home import cards_home
def home()-> rx.Component:
    return rx.box(
        nadbar(),
        rx.grid(
            # cada tarjeta es un hijo directo del grid
            cards_home("Total de Materiales", 5, "box", "#457B9D", "#1D3557"),
            cards_home("Disponibles", 3, "chart_spline", "#22C55E", "#15803D"),
            cards_home("Agotados", 1, "triangle_alert", "#EF4444", "#B91C1C"),
            cards_home("En Reposicion", 1, "shopping_cart", "#EAB308", "#A16207"),
            # grid responsivo: cada columna tendrá al menos 200px y crecerá proporcionalmente
            columns="4",
            gap="1.5rem",
            padding_x="4rem",
            margin_top="2rem",
            
            
        ),
    )