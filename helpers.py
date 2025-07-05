import time
from selenium.webdriver.support import expected_conditions as EC


def wait_and_click(driver, locator, wait):
    element = wait.until(EC.element_to_be_clickable(locator))
    driver.execute_script("arguments[0].click();", element)


def wait_for_element(driver, locator, wait):
    return wait.until(EC.presence_of_element_located(locator))


def simulate_tab(element):
    element.send_keys("\t")
    time.sleep(0.5)
