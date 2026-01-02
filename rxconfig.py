import reflex as rx

config = rx.Config(
    app_name="Inventario",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    state_auto_setters=False,
)