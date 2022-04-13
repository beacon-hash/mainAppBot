from selenium import webdriver
from mainapp.constants import *
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from mainapp.text_match import text_match
import re

class Assign:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.assignment_logger = logging.getLogger("Assignment")

    def check_assignment(self, serial_number):
        assigned = False
        container_box = self.driver.find_element(
            By.XPATH,
            '//*[@id="CPB_I4"]/div[1]'
        )
        child_elements = container_box.find_elements(
            By.CSS_SELECTOR,
            '*'
        )
        for element in child_elements:
            if element.get_attribute('id') == "CPB_cmdReleaseEmpl":
                assigned = True
                assigned_user = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="CPB_divAssignTo"]/ul/li[1]/b'
                )
                self.assignment_logger.warning(f"{serial_number} is already assigned to {assigned_user.text}.")
                break
            else:
                assigned = False
        return assigned
    
    def do_assignment(self,serial_number, employee_id):
        select_user = self.driver.find_element(
            By.ID,
            'CPB_cmdSelectUser'
        )
        select_user.click()
        search_user_field = self.driver.find_element(
            By.ID,
            'CPB_txtEmpCriteria'
        )
        search_user_field.clear()
        search_user_field.send_keys(employee_id)
        search_user_button = self.driver.find_element(
            By.ID,
            'CPB_cmdEmpSearch'
        )
        search_user_button.click()
        WebDriverWait(self.driver, TIMEOUT).until(
            text_match(
                (By.ID, 'CPB_divMsg'),
                r"(We could not|activities)"
            )
        )
        message_area = self.driver.find_element(
                By.ID,
                'CPB_divMsg'
            )
        if re.search(r"activities", message_area.text):
            selected_user_button = self.driver.find_element(
                By.ID,
                'CPB_gvSem_cmdSelectEmp_0'
            )
            selected_user_button.click()
            submit_user_assignment = self.driver.find_element(
                By.ID,
                'CPB_cmdSaveEmpl'
            )
            submit_user_assignment.click()
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.text_to_be_present_in_element(
                    (By.ID, 'CPB_divMsg'),
                    '. Processing has been completed successfully.'
                )
            )
            assigned_user = self.driver.find_element(
                By.XPATH,
                '//*[@id="CPB_divMsg"]/b'
            )
            self.assignment_logger.info(f"{serial_number} is assigned to {assigned_user.text} successfully.")
        else:
            raise TimeoutException