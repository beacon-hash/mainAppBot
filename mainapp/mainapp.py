from email import message
from mainapp.constants import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from mainapp.itemassignment import Assign
from mainapp.itemregistration import Enroll
from mainapp.itemrelease import Release
from mainapp.itemmovement import Move
import logging
from msedge.selenium_tools import EdgeOptions
import re
from msedge.selenium_tools import Edge
from mainapp.text_match import text_match
from selenium.common.exceptions import TimeoutException



class MainApp(Edge):
    def __init__(self, teardown=False, headless=True):
        self.headless = headless
        self.teardown = teardown
        if headless:
            self.msedge_options = EdgeOptions()
            self.msedge_options.use_chromium = True
            self.msedge_options.add_argument("--headless")
            self.msedge_options.add_argument("--disable-gpu")
            self.msedge_options.add_argument("--log-level=3")
            # self.chrome_options = Options()
            # self.chrome_options.headless = headless
            # self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            super(MainApp, self).__init__(executable_path=EDGE_DRIVER, options=self.msedge_options)
        else:
            super(MainApp, self).__init__(executable_path=EDGE_DRIVER)
        self.assigner = Assign(driver=self)
        self.releaser = Release(driver=self)
        self.mover = Move(driver=self)
        self.enroller = Enroll(driver=self)
        self.implicitly_wait(TIMEOUT)
        self.maximize_window()
        self.main_logger = logging.getLogger("Main")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(BASE_URL)

    def sign_in(self, username, password):
        username_element = self.find_element(
            By.ID,
            'txtUserName'
        )
        username_element.clear()
        username_element.send_keys(username)
        password_element = self.find_element(
            By.ID,
            'txtPassword'
        )
        password_element.clear()
        password_element.send_keys(password)
        sign_in_element = self.find_element(
            By.ID,
            'cmdSignIn'
        )
        sign_in_element.click()

    def isexist(self, serial_number, selection):
        manage_serial_number = self.find_element(
            By.ID,
            'CPB_searchVarItemSerialNumber'
        )
        manage_serial_number.clear()
        manage_serial_number.send_keys(serial_number)
        manage_serial_number_search = self.find_element(
            By.ID,
            'CPB_cmdLoadSearch'
        )
        manage_serial_number_search.click()
        
        WebDriverWait(self, TIMEOUT, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            text_match(
                (By.ID, 'CPB_divMsg'),
                r"(Displaying|We could not)"
            )
        )
        message_area = self.find_element(
            By.ID,
            'CPB_divMsg'
        )
        if re.search(r"Displaying", message_area.text) and selection == "E":
            assets_tool_tab = self.find_element(
                    By.ID,
                    'LB1'
                )
            assets_tool_tab.click()
            manage_assets_tab = self.find_element(
                By.ID,
                'cmdMngAss'
            )
            manage_assets_tab.click()
            return True
        elif re.search(r"Displaying", message_area.text):
            return True
        else:
            self.main_logger.warning(f"{serial_number} doesn't exist.")
            if selection == "M":
                self.mover.load_move_assets_page()
            elif selection == "A" or selection == "R" or selection == "E":
                assets_tool_tab = self.find_element(
                    By.ID,
                    'LB1'
                )
                assets_tool_tab.click()
                manage_assets_tab = self.find_element(
                    By.ID,
                    'cmdMngAss'
                )
                manage_assets_tab.click()
            return False


    def select_asset(self, serial_number):
        message_area = self.find_element(
            By.ID,
            'CPB_divMsg'
        )
        x = re.findall(r"[0-9]+", message_area.text)        
        if int(x[0]) > 1:
            self.main_logger.warning(f"{serial_number} has multiple entries - Please, check it.")
            assets_tool_tab = self.find_element(
                By.ID,
                'LB1'
            )
            assets_tool_tab.click()
            manage_assets_tab = self.find_element(
                By.ID,
                'cmdMngAss'
            )
            manage_assets_tab.click()
            raise TimeoutException
        else:
            select_asset = self.find_element(
                By.ID,
                'CPB_dgMyItems_cmdSelectItem_0'
            )
            select_asset.click()
            asset_assignment = self.find_element(
                By.ID,
                'CPB_LB4'
            )
            asset_assignment.click()

    def isassigned(self, serial_number):
        return self.assigner.check_assignment(serial_number)

    def assign(self, serial_number, employee_id):
        self.assigner.do_assignment(serial_number, employee_id)
    
    def release(self, serial_number):
        self.releaser.do_release(serial_number)
    
    def move(self, serial_number, destination):
        self.mover.do_movement(serial_number, destination)

    def load_movement_page(self):
        self.mover.load_move_assets_page()
    
    def load_register_page(self):
        self.enroller.load_register_assets_page()
    
    def enroll(self, serial_number, asset_tag, po_number, manfacturer, model, destination):
        self.enroller.do_enrollment(serial_number, asset_tag, po_number, manfacturer, model, destination)