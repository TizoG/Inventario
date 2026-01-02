import reflex as rx

def cards_home(title: str, value: int, icon:str, color: str, gradient: str)-> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(title),
            rx.text(value, font_size="2xl", font_weight="bold"),
            rx.icon(icon, color="white", font_size="4xl"),
            
        ),
        padding="1rem",
        border="1px solid #ccc",
        border_radius="8px",
        box_shadow="md",
        width="100%",
        height="150px",
        bg="linear-gradient(135deg, {color}, {gradient})".format(color=color, gradient=gradient),
        color="white",
        cursor="pointer",
        _hover={
            "box_shadow": "0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04)",
            
        }

    ),