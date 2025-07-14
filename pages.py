from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import data
from helpers import retrieve_phone_code

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    card_number_field = (By.ID, "number")
    cvv_field = (By.NAME, "code")
    confirm_card_button = (By.XPATH, "//button[normalize-space()='Agregar']")

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

        try:
            code_input = self.wait.until(EC.presence_of_element_located((By.ID, "code")))
            confirmation_code = retrieve_phone_code(self.driver)
            code_input.send_keys(confirmation_code)

            confirmar_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Confirmar']")
            ))
            self.driver.execute_script("arguments[0].click();", confirmar_btn)
        except Exception as e:
            print("No se completó la confirmación del código telefónico:", e)

    def open_payment_method(self):
        metodo_pago = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'pp-button') and .//div[text()='Método de pago']]")
        ))
        self.driver.execute_script("arguments[0].click();", metodo_pago)

    def click_add_card_button(self):
        opcion_tarjeta = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Agregar tarjeta')]")
        ))
        self.driver.execute_script("arguments[0].click();", opcion_tarjeta)

    def click_card(self, card_number):
        self.driver.implicitly_wait(30)
        card_input = self.driver.find_element(*self.card_number_field)
        card_input.click()
        card_input.send_keys(card_number)

    def add_code_card(self, cvv):
        self.driver.implicitly_wait(10)
        code_input = self.driver.find_element(*self.cvv_field)
        code_input.click()
        code_input.send_keys(cvv + Keys.TAB)
        time.sleep(1)

    def card_submit_button(self):
        self.driver.implicitly_wait(10)
        agregar = self.wait.until(EC.element_to_be_clickable(self.confirm_card_button))
        agregar.click()
        self.cerrar_ventana_confirmacion_tarjeta()

        self.escribir_mensaje_para_conductor(data.message_for_driver)
        self.activar_manta_y_panuelos()
        time.sleep(1)

    def cerrar_ventana_confirmacion_tarjeta(self):
        try:
            cerrar_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
            ))
            self.driver.execute_script("arguments[0].click();", cerrar_btn)
        except Exception as e:
            print("No se pudo cerrar la ventana de tarjeta:", e)

    def escribir_mensaje_para_conductor(self, mensaje):
        input_mensaje = self.wait.until(EC.element_to_be_clickable((By.ID, "comment")))
        input_mensaje.clear()
        input_mensaje.send_keys(mensaje)

    def activar_manta_y_panuelos(self):
        slider = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
        ))
        self.driver.execute_script("arguments[0].click();", slider)
        activo = slider.get_attribute("aria-checked")
        assert activo == "true", "La manta y pañuelos no fueron activados"

    def pedir_dos_helados(self):
        boton_plus = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton_plus)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", boton_plus)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", boton_plus)
        cantidad_helados = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='counter-value' and text()='2']")
        ))
        assert cantidad_helados.is_displayed(), "No se seleccionaron dos helados"

    def confirmar_pedido(self):
        boton_confirmar = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')
        ))
        self.driver.execute_script("arguments[0].click();", boton_confirmar)

    def esperar_info_conductor(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Buscando un conductor')]")
            ))
            conductor = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(),'Tu conductor') or contains(text(),'viene a recogerte')]")
            ))
            return conductor
        except Exception as e:
            print("No se pudo obtener la información del conductor:", e)
            return None



