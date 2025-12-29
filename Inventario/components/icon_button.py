import reflex as rx

def icon_button(icon : str, href : str) -> rx.Component:
    return rx.icon_button(
        icon,
        variant="ghost",
        cursor="pointer",
        color="white",
        _hover={
            "bg":"#457B9D"
        },
        href=href,

    )