from selenium.webdriver.support.expected_conditions import _find_element
import re

class text_match(object):
    def __init__(self, locator, regexp):
        self.locator = locator
        self.regexp = regexp

    def __call__(self, driver):
        element_text = _find_element(driver, self.locator).text
        return re.search(self.regexp, element_text)

