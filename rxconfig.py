import reflex as rx

config = rx.Config(
    app_name="Inventario",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    # Evita la generación automática de setters (después de la deprecación)
    state_auto_setters=False,
)