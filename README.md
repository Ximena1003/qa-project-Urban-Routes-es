#Proyecto Sprint 8
## Ximena Carmona
### Automatización de pruebas de la aplicación web
### Grupo 28


# Pagina para pruebas Urban Routes – Automatización de Pruebas con Selenium
Automatización, flujo de prueba completo en la aplicación web Urban Routes.
Está desarrollado en Python utilizando Selenium WebDriver y Pytest.

## Descripción del Proyecto
Este proyecto QA automatiza la interacción de un usuario con el servicio Urban Routes.
solicitud de taxi, elección de tarifa, ingreso de teléfono, método de pago, solicitud de artículos
adicionales y confirmación de pedido

### Herramientas Usadas
- Python 3.13
- Selenium WebDriver
- Pytest
- Google Chrome + Chromedriver
- Page Object Model (POM)

### metodo de instalación
descargadas por Python packages

#### Estructura del Proyecto
main.py # Contiene la clase UrbanRoutesPage y las pruebas TestUrbanRoutes
data.py # Contiene datos de prueba como direcciones, número de teléfono, tarjeta y mensaje
pages.py # Contiene la clase UrbanRoutesPage con todos los localizadores y acciones
helpers.py # Contiene las funciones auxiliares 
README.md # Este archivo, donde de hace la trazabilidad de la ejecución de las pruebas

##### Descripción del flujo
- Ingresar dirección de origen y destino.
- Pedir taxi
- Seleccionar la tarifa `Comfort`.
- Introducir el número de teléfono de el usuario.
- Cerrar ventanas emergentes si aparecen.
- Seleccionar "Método de pago" y añadir una tarjeta.
quedo (pausa manual de 10 segundos, para ingresar CVV y dar clic en "Agregar").
- Escribir un mensaje para el conductor.
- Activar la opción "Manta y pañuelos".
- Añadir dos helados al pedido.
- Buscar conductor
- Confirmacion de tiempo en que llagara el conductor e informacion del carro

###### Ejecución de las pruebas (terminal)

pytest main.py