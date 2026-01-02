# Inventario

Inventario es una aplicación ligera en Python para la gestión y control básico de existencias. Provee una estructura de proyecto organizada para almacenar, consultar y visualizar elementos del inventario, pensada como base para aplicaciones de escritorio o web pequeñas y como ejemplo didáctico para desarrolladores.

**Público objetivo**
- Desarrolladores que necesitan una base para construir una solución de inventario.
- Equipos pequeños que desean un prototipo rápido para control de stock.
- Estudiantes que aprenden a estructurar proyectos Python con persistencia de datos.

**Características principales**
- Estructura modular con la lógica del inventario separada en el paquete `Inventario`.
- Scripts de ejemplo para poblar datos (`agregar_datos_ejemplo.py`).
- Documentación y pasos de instalación para preparar la base de datos (`BD_SETUP.md`).

## Requisitos

- Python 3.10+ (ver `requirements.txt` para dependencias específicas)

## Instalación rápida

1. Clona el repositorio:

   git clone <url-del-repositorio>
   cd Inventario

2. Crea y activa un entorno virtual (recomendado):

   python -m venv .venv
   source .venv/bin/activate

3. Instala dependencias:

   pip install -r requirements.txt

4. Sigue las instrucciones de configuración de la base de datos:

   - Revisa [BD_SETUP.md](BD_SETUP.md) para configurar la base de datos local.
   - Usa `agregar_datos_ejemplo.py` para poblar datos de ejemplo si lo deseas:

     python agregar_datos_ejemplo.py

## Uso

El repositorio contiene la lógica principal dentro del paquete `Inventario`. Dependiendo de cómo desees desplegar la aplicación (CLI, GUI o web), usa los módulos bajo `Inventario/`:

- `Inventario/database.py`: abstracciones y conexión a la base de datos.
- `Inventario/Inventario.py` y `Inventario/state.py`: lógica del dominio y estado.
- `Inventario/pages/` y `Inventario/components/`: vistas y componentes (útiles si integras con frameworks tipo Streamlit o Flask).

Para comenzar rápidamente:

- Configura la base de datos según `BD_SETUP.md`.
- Ejecuta `python agregar_datos_ejemplo.py` para probar con datos de ejemplo.
- Integra o crea un punto de entrada (por ejemplo, un script Flask o Streamlit) que importe `Inventario` y exponga UI.

## Estructura del proyecto

- `agregar_datos_ejemplo.py`: script para insertar datos de ejemplo.
- `BD_SETUP.md`: guía para inicializar la base de datos.
- `requirements.txt`: dependencias del proyecto.
- `Inventario/`: paquete principal con la lógica y componentes.
  - `database.py` — conexión y utilidades DB
  - `Inventario.py` — modelo/servicios principales
  - `state.py` — gestión de estado
  - `components/` — componentes UI reutilizables
  - `pages/` — páginas/escenas de la aplicación

## Contribuir

1. Abre un issue para describir el cambio que propones.
2. Crea una rama con nombre descriptivo `feature/mi-cambio`.
3. Envía un pull request con una descripción clara y pruebas o instrucciones para replicar.

## Buenas prácticas de desarrollo

- Trabaja en entorno virtual para aislar dependencias.
- Añade pruebas unitarias cuando añadas lógica crítica.
- Mantén separada la lógica de negocio de la presentación para facilitar reutilización.

## Soporte y contacto

Si encuentras problemas o quieres colaborar, abre un issue en el repositorio o contacta al mantenedor (ver metadata del repositorio).

## Licencia

Este proyecto está bajo la licencia incluida en el repositorio (`LICENSE`).

## Notas finales

Este README ofrece una guía de inicio rápida y orientada a desarrolladores. Si quieres, puedo:

- Añadir un ejemplo mínimo de arranque (un pequeño servidor Flask o una app Streamlit).
- Crear tests iniciales o un archivo `Makefile` para tareas comunes.

Dime qué prefieres y lo preparo.
# Inventario
App para gestión de inventario. 
