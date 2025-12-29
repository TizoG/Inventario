import reflex as rx

from ..components.nadbar import nadbar

def home()-> rx.Component:
    return rx.box(
        nadbar()
    )