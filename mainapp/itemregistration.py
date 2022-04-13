from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from mainapp.constants import *




class Enroll:
    def __init__(self, driver: webdriver.Edge):
        self.driver = driver 
        self.enrollment_logger = logging.getLogger("Enrollment")
    
    def load_register_assets_page(self):
        asset_tools = self.driver.find_element(
            By.ID,
            'LB1'
        )
        asset_tools.click()
        register_asset = self.driver.find_element(
            By.ID,
            'cmdRegAss'
        )
        register_asset.click()
    
    def wait_until(self, ID):
        WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.element_to_be_clickable(
                (By.ID, ID)
            )
        )
    
    def do_enrollment(self, serial_number, asset_tag, po_number, manfacturer, model, destination):
        location = "EGY - Alexandria [Alexandria]"
        if destination == "S7A":
            floor = "EGYPT7"
            section = "EGY7-Production A"
            subsection = "EGY7-100"
            status = "In Use (I)"
            dest = "7th Floor - Production A"
        elif destination == "H":
            floor = "EGYPT"
            section = "Work at Home"
            subsection = "EGY-WAH ASSETS"
            status = "In Use (I)"
            dest = "Work at Home"
        elif destination == "S7B":
            floor = "EGYPT7"
            section = "EGY7-Production B"
            subsection = "EGY7-010"
            status = "In Use (I)"
            dest = "7th Floor - Production B"
        elif destination == "S6A":
            floor = "EGYPT6"
            section = "EGY6-Production A"
            subsection = "EGY6-010"
            status = "In Use (I)"
            dest = "6th Floor - Production A"
        elif destination == "G":
            floor = "EGYPT8"
            section = "GTI OPS"
            subsection = "EGY-GTISTK"
            status = "In Use (I)"
            dest = "GTI Stock"
        elif destination == "L":
            floor = "EGYPT"
            section = "Laptops and Tablets"
            subsection = "EGY-LAPTOPS"
            status = "In Use (I)"
            dest = "Laptops"

        select_location = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtIntLocIDN'
            )
        )
        select_location.select_by_visible_text(location)
        self.wait_until('CPB_txtIntFloorIDN')

        select_floor = Select(
                self.driver.find_element(
                    By.ID,
                    'CPB_txtIntFloorIDN'
                )
            )

        select_floor.select_by_visible_text(floor)
        self.wait_until('CPB_txtIntSecIDN')

        select_section = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtIntSecIDN'
            )
        )
        select_section.select_by_visible_text(section)
        self.wait_until('CPB_txtIntSubIDN')

        select_subsection = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtIntSubIDN'
            )
        )
        select_subsection.select_by_visible_text(subsection)
        self.wait_until('CPB_txtIntMakeIDN')

        select_manfacturer = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtIntMakeIDN'
            )
        )
        select_manfacturer.select_by_visible_text(manfacturer)
        self.wait_until('CPB_txtIntModelIDN')

        select_model = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtIntModelIDN'
            )
        )
        select_model.select_by_visible_text(model)
        self.wait_until('CPB_txtIntStatusIDN')

        select_status = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtIntStatusIDN'
            )
        )
        select_status.select_by_visible_text(status)

        select_ownership = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtVarOwnership'
            )
        )
        select_ownership.select_by_visible_text("Sutherland")

        select_bu = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtVarBusinessUnit'
            )
        )
        select_bu.select_by_visible_text("EGY01 - SGS - Egypt")

        po_field = self.driver.find_element(
            By.ID,
            'CPB_txtVarItemPONumber'
        )
        po_field.send_keys(po_number)

        asset_tag_field = self.driver.find_element(
            By.ID,
            'txtVarItemTag'
        )
        asset_tag_field.send_keys(asset_tag)

        serial_number_field = self.driver.find_element(
            By.ID,
            'txtVarItemSerialNumber'
        )
        serial_number_field.send_keys(serial_number)

        save_button = self.driver.find_element(
            By.ID,
            'CPB_cmdRegItemSave2'
        )
        save_button.click()
        try:
            WebDriverWait(self.driver, timeout=TIMEOUT, ignored_exceptions=IGNORED_EXCEPTIONS).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, '//*[@id="CPB_divReport"]/div/table/tbody/tr/td[2]'),
                    serial_number.upper()
                )
            )
            self.enrollment_logger.info(f"{serial_number} has been registered successfully.")
        except TimeoutException:
            self.enrollment_logger.warning(f"Can't register {serial_number} as it's already registered with {asset_tag}.")

        

