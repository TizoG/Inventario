"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from .pages.home import home

from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    return rx.box(
        home(),

    )


app = rx.App()
app.add_page(index)
