import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def set_route(self, from_address, to_address):
        from_input = self.wait.until(EC.visibility_of_element_located(self.from_field))
        from_input.clear()
        from_input.send_keys(from_address)
        from_input.send_keys(Keys.RETURN)

        to_input = self.wait.until(EC.visibility_of_element_located(self.to_field))
        to_input.clear()
        to_input.send_keys(to_address)
        to_input.send_keys(Keys.RETURN)

    def order_taxi(self):
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")
        ))
        self.driver.execute_script("arguments[0].click();", button)

    def select_comfort_tariff(self):
        comfort_card = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'tcard-title') and text()='Comfort']")
        ))
        tcard = comfort_card.find_element(By.XPATH, "./ancestor::div[contains(@class, 'tcard')]")
        button = tcard.find_element(By.TAG_NAME, "button")
        self.driver.execute_script("arguments[0].click();", button)

    def enter_phone_number(self, phone_number):
        phone_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='np-button' and .//div[text()='Número de teléfono']]")
        ))
        self.driver.execute_script("arguments[0].click();", phone_button)

        phone_input = self.wait.until(EC.visibility_of_element_located((By.ID, "phone")))
        phone_input.clear()
        phone_input.send_keys(phone_number)

        siguiente_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Siguiente']")
        ))
        self.driver.execute_script("arguments[0].click();", siguiente_button)

    def cerrar_ventana_emergente(self):
        try:
            close_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/button')
            ))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", close_button)
        except Exception as e:
            print("No se pudo cerrar la ventana:", e)

    def click_metodo_pago(self):
        metodo_pago = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'pp-button') and .//div[text()='Método de pago']]")
        ))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", metodo_pago)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", metodo_pago)

    def seleccionar_agregar_tarjeta(self):
        opcion_tarjeta = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Agregar tarjeta')]")
        ))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", opcion_tarjeta)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", opcion_tarjeta)

    def ingresar_datos_tarjeta(self, numero):
        input_numero = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "number")
        ))
        input_numero.clear()
        input_numero.send_keys(numero)

        print("Pausa para ingresar el código 111 manualmente...")
        time.sleep(10)  # Tiempo para escribir manualmente 111 y dar clic en Agregar

    def cerrar_ventana_confirmacion_tarjeta(self):
        try:
            cerrar_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
            ))
            self.driver.execute_script("arguments[0].click();", cerrar_btn)
        except Exception as e:
            print("No se pudo cerrar la ventana de tarjeta:", e)

    def escribir_mensaje_para_conductor(self, mensaje):
        input_mensaje = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="comment"]')
        ))
        input_mensaje.clear()
        input_mensaje.send_keys(mensaje)

    def activar_manta_y_panuelos(self):
        slider = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
        ))
        self.driver.execute_script("arguments[0].click();", slider)

    def pedir_dos_helados(self):
        boton_plus = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
        ))
        self.driver.execute_script("arguments[0].click();", boton_plus)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", boton_plus)

    def confirmar_pedido(self):
        boton_confirmar = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')
        ))
        self.driver.execute_script("arguments[0].click();", boton_confirmar)


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

    def test_click_order_taxi_and_add_card(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)

        page.set_route(data.address_from, data.address_to)
        page.order_taxi()
        page.select_comfort_tariff()
        page.enter_phone_number(data.phone_number)

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//button[normalize-space()='Siguiente']"))
        )
        time.sleep(1)

        page.cerrar_ventana_emergente()
        page.click_metodo_pago()
        page.seleccionar_agregar_tarjeta()
        page.ingresar_datos_tarjeta(data.card_number)

        # Pausa manual para ingresar CVV y clic en "Agregar"
        page.cerrar_ventana_confirmacion_tarjeta()
        page.escribir_mensaje_para_conductor(data.message_for_driver)
        page.activar_manta_y_panuelos()
        page.pedir_dos_helados()
        page.confirmar_pedido()

        time.sleep(5)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
