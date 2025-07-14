import data
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class TestUrbanRoutes:
    driver = None
    page = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.page = UrbanRoutesPage(cls.driver)
        cls.driver.get(data.urban_routes_url)

    def test_01_set_route(self):
        self.page.set_route(data.address_from, data.address_to)
        value = self.page.driver.find_element(*self.page.to_field).get_attribute("value")
        assert value.strip() != "", "El campo de destino no fue llenado correctamente"

    def test_02_order_taxi(self):
        self.page.order_taxi()
        comfort = self.page.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'tcard-title') and text()='Comfort']")
        ))
        assert comfort, "No se cargó la tarjeta 'Comfort'"

    def test_03_select_comfort_tariff(self):
        self.page.select_comfort_tariff()
        phone_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "phone"))
        )
        assert phone_field and phone_field.is_displayed(), "No se mostró el campo de teléfono"

    def test_04_enter_phone_number(self):
        self.page.enter_phone_number(data.phone_number)
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//button[normalize-space()='Siguiente']"))
        )

    def test_05_open_payment_method(self):
        self.page.open_payment_method()

    def test_06_click_add_card_button(self):
        self.page.click_add_card_button()

    def test_07_add_card_data(self):
        self.page.click_card(data.card_number)
        self.page.add_code_card(data.card_code)
        self.page.card_submit_button()
        metodo = self.page.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='pp-value-text' and contains(text(),'****')]")
        ))
        assert metodo and "****" in metodo.text, "No se agregó correctamente la tarjeta"

    def test_08_validar_mensaje(self):
        mensaje = self.page.driver.find_element(By.ID, "comment").get_attribute("value")
        assert mensaje == data.message_for_driver, "El mensaje no se escribió correctamente"

    def test_09_validar_manta_y_panuelos(self):
        slider = self.page.driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span'
        )
        estado = slider.get_attribute("aria-checked")
        assert estado == "true", "La manta y pañuelos no están activados"

    def test_10_pedir_dos_helados(self):
        self.page.pedir_dos_helados()

    def test_11_confirmar_pedido(self):
        self.page.confirmar_pedido()
        modal = self.page.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(),'Buscando un conductor')]")
        ))
        assert modal.is_displayed(), "No apareció el modal de búsqueda de conductor"

    def test_12_esperar_info_conductor(self):
        conductor = self.page.esperar_info_conductor()
        assert conductor is not None and conductor.is_displayed(), "No se mostró la información del conductor"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()