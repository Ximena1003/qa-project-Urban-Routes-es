from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

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
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")))
        self.driver.execute_script("arguments[0].click();", button)

    def select_comfort_tariff(self):
        comfort_card = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'tcard-title') and text()='Comfort']")))
        tcard = comfort_card.find_element(By.XPATH, "./ancestor::div[contains(@class, 'tcard')]")
        button = tcard.find_element(By.TAG_NAME, "button")
        self.driver.execute_script("arguments[0].click();", button)

    def enter_phone_number(self, phone_number):
        phone_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='np-button' and .//div[text()='Número de teléfono']]")))
        self.driver.execute_script("arguments[0].click();", phone_button)

        phone_input = self.wait.until(EC.visibility_of_element_located((By.ID, "phone")))
        phone_input.clear()
        phone_input.send_keys(phone_number)

        siguiente_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Siguiente']")))
        self.driver.execute_script("arguments[0].click();", siguiente_button)

    def cerrar_ventana_emergente(self):
        try:
            close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/button')))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
            self.driver.execute_script("arguments[0].click();", close_button)
        except Exception:
            pass

    def click_metodo_pago(self):
        metodo_pago = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pp-button') and .//div[text()='Método de pago']]")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", metodo_pago)
        self.driver.execute_script("arguments[0].click();", metodo_pago)

    def seleccionar_agregar_tarjeta(self):
        opcion_tarjeta = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Agregar tarjeta')]")))
        self.driver.execute_script("arguments[0].click();", opcion_tarjeta)

    def ingresar_datos_tarjeta(self, numero):
        input_numero = self.wait.until(EC.visibility_of_element_located((By.ID, "number")))
        input_numero.clear()
        input_numero.send_keys(numero)

    def cerrar_ventana_confirmacion_tarjeta(self):
        try:
            cerrar_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')))
            self.driver.execute_script("arguments[0].click();", cerrar_btn)
        except Exception:
            pass

    def escribir_mensaje_para_conductor(self, mensaje):
        input_mensaje = self.wait.until(EC.element_to_be_clickable((By.ID, "comment")))
        input_mensaje.clear()
        input_mensaje.send_keys(mensaje)

    def activar_manta_y_panuelos(self):
        slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')))
        self.driver.execute_script("arguments[0].click();", slider)

    def pedir_dos_helados(self):
        boton_plus = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')))
        self.driver.execute_script("arguments[0].click();", boton_plus)
        self.driver.execute_script("arguments[0].click();", boton_plus)

    def confirmar_pedido(self):
        boton_confirmar = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')))
        self.driver.execute_script("arguments[0].click();", boton_confirmar)

    def esperar_info_conductor(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(text(),'Buscando un conductor')]")))
            conductor = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Tu conductor') or contains(text(),'viene a recogerte')]")))
            return conductor
        except Exception:
            return None