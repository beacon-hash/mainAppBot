from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mainapp.constants import *


class Release:
    def __init__(self, driver: webdriver.Edge):
        self.driver = driver 
        self.release_logger = logging.getLogger("Release")
    
    def do_release(self, serial_number):
        release_asset_button = self.driver.find_element(
            By.ID,
            'CPB_cmdReleaseEmpl'
        )
        release_asset_button.click()
        WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="CPB_divMsg"]/b'),
                'Available'
            )
        )
        self.release_logger.info(f"{serial_number} is released from the user.")
