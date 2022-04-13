from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

EDGE_DRIVER = r"C:\SeleniumDrivers\msedgedriver.exe"
BASE_URL = "https://mainapp.sutherlandglobal.com"
TIMEOUT = 10
IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)