from selenium import webdriver
from mainapp.constants import *
from selenium.webdriver.common.by import By
import logging 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select



class Move:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver 
        self.movement_logger = logging.getLogger("Movement")
    
    def load_move_assets_page(self):
        asset_tools = self.driver.find_element(
            By.ID,
            'LB1'
        )
        asset_tools.click()
        move_assets = self.driver.find_element(
            By.ID,
            'cmdMovAss'
        )
        move_assets.click()

    def wait_until(self, ID):
        WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.element_to_be_clickable(
                (By.ID, ID)
            )
        )

    def select_destination(self, destination):
        location = "EGY - Alexandria"
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
        self.wait_until('CPB_txtIntStatusIDN')

        select_status = Select(
            self.driver.find_element(
                By.ID,
                'CPB_txtIntStatusIDN'
            )
        )
        select_status.select_by_visible_text(status)

        return dest



    def do_movement(self, serial_number, destination):
        # location = "EGY - Alexandria"
        # if destination == "S7A":
        #     floor = "EGYPT7"
        #     section = "EGY7-Production A"
        #     subsection = "EGY7-100"
        #     status = "In Use (I)"
        #     dest = "7th Floor - Production A"
        # elif destination == "H":
        #     floor = "EGYPT"
        #     section = "Work at Home"
        #     subsection = "EGY-WAH ASSETS"
        #     status = "In Use (I)"
        #     dest = "Work at Home"
        # elif destination == "S7B":
        #     floor = "EGYPT7"
        #     section = "EGY7-Production B"
        #     subsection = "EGY7-010"
        #     status = "In Use (I)"
        #     dest = "7th Floor - Production B"
        # elif destination == "S6A":
        #     floor = "EGYPT6"
        #     section = "EGY6-Production A"
        #     subsection = "EGY6-010"
        #     status = "In Use (I)"
        #     dest = "6th Floor - Production A"
        # elif destination == "G":
        #     floor = "EGYPT8"
        #     section = "GTI OPS"
        #     subsection = "EGY-GTISTK"
        #     status = "In Use (I)"
        #     dest = "GTI Stock"
        # elif destination == "L":
        #     floor = "EGYPT"
        #     section = "Laptops and Tablets"
        #     subsection = "EGY-LAPTOPS"
        #     status = "In Use (I)"
        #     dest = "Laptops"

        # select_location = Select(
        #     self.driver.find_element(
        #         By.ID,
        #         'CPB_txtIntLocIDN'
        #     )
        # )
        # select_location.select_by_visible_text(location)
        # self.wait_until('CPB_txtIntFloorIDN')

        # select_floor = Select(
        #         self.driver.find_element(
        #             By.ID,
        #             'CPB_txtIntFloorIDN'
        #         )
        #     )

        # select_floor.select_by_visible_text(floor)
        # self.wait_until('CPB_txtIntSecIDN')

        # select_section = Select(
        #     self.driver.find_element(
        #         By.ID,
        #         'CPB_txtIntSecIDN'
        #     )
        # )
        # select_section.select_by_visible_text(section)
        # self.wait_until('CPB_txtIntSubIDN')

        # select_subsection = Select(
        #     self.driver.find_element(
        #         By.ID,
        #         'CPB_txtIntSubIDN'
        #     )
        # )
        # select_subsection.select_by_visible_text(subsection)
        # self.wait_until('CPB_txtIntStatusIDN')

        # select_status = Select(
        #     self.driver.find_element(
        #         By.ID,
        #         'CPB_txtIntStatusIDN'
        #     )
        # )
        # select_status.select_by_visible_text(status)
        dest = self.select_destination(destination=destination)
        select_all = self.driver.find_element(
            By.ID,
            'selectall'
        )
        select_all.click()
        move_button = self.driver.find_element(
            By.ID,
            'CPB_cmdMoveSave'
        )
        move_button.click()
        WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.text_to_be_present_in_element(
                (By.ID, 'CPB_divMsg'),
                'completed successfully.'
            )
        )
        self.movement_logger.info(f"{serial_number} is moved to {dest} successfully.")

        # except StaleElementReferenceException:
        #     print("ERROR: Something went wrong. Please, re-run the bot again.")
        #     helper = Helper()
        #     helper.closure()
            


        

