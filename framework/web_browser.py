from typing import Any
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from framework.ui_elements import Locator
from framework.logger import get_logger
from framework.utils import retry_on_empty_result
from selenium.webdriver.common.action_chains import ActionChains

logger = get_logger()


def _create_driver(browser: str):
    """ returns webdriver """

    return _get_local_driver(browser)


@retry_on_empty_result()
def _get_local_driver(browser: str):
    """ returns local webdriver """
    match browser:
        case "firefox":
            options = webdriver.FirefoxOptions()
            driver = webdriver.Firefox(options=options)
        case "edge":
            options = webdriver.EdgeOptions()
            driver = webdriver.Edge(options=options)
        case "chrome":
            options = ChromeOptions()
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=options)
        case _:
            raise ValueError(f"Unexpected value {browser}")
    logger.info(f'Creating local driver of {browser} type')
    logger.info(f'Driver: {driver}')
    return driver


class Actions:

    def __init__(self, driver):
        self.driver = driver
        self.action = ActionChains(driver)

    def press_enter(self) -> None:
        self.action.send_keys(Keys.ENTER).perform()


class WebBrowser:
    """ Responsible for all web browser capabilities """

    def __init__(self, browser: str):
        logger.info(
            f"Calling {_create_driver} with browser: {browser}")
        self.driver = _create_driver(browser)
        self.wait = Wait(self.driver)
        self.actions = Actions(self.driver)

    @property
    def name(self) -> str:
        return self.driver.name

    @property
    def capabilities(self) -> dict:
        return self.driver.capabilities

    def quit_driver(self):
        """ Quits the WebDriver """
        if self.driver:
            self.driver.quit()

    def get(self, url: str):
        """ gets url and validates page url """
        self.driver.get(url)

    def refresh(self):
        """ refreshes the page """
        self.driver.refresh()

    def get_current_url(self) -> str:
        """ returns current url """
        return self.driver.current_url

    def find_element(self, locator: Locator) -> WebElement:
        """
        find element and returns WebElement object
        :type locator: object
        :return: Web element
        """
        logger.info(f"finding element, {locator.__repr__()}")
        return self.driver.find_element(*locator)

    def find_elements(self, locator: Locator) -> list[WebElement]:
        """
        find element and returns WebElement object
        :type locator: object
        :return: Web element
        """
        logger.info(f"finding elements, {locator.__repr__()}")
        return self.driver.find_elements(*locator)

    def click(self, locator: Locator) -> None:
        """
        Finds an element using locator
        waits until element is clickable
        clicks the element
        """
        element = self.wait.until_clickable(locator)
        element.click()

    def get_text(self, locator: Locator) -> str:
        """
        returns element's text
        """
        return self.find_element(locator).text

    def get_screenshot_as_png(self) -> bytes:
        """
        captures a full screenshot as png format
        """
        return self.driver.get_screenshot_as_png()

    def execute_js(self, script) -> Any:
        """
        execute js script
        :param script:
        :return: Any
        """
        return self.driver.execute_script(script)

    def execute_script(self, script, element) -> Any:
        """
        execute js on a specific element
        :param script:
        :param element:
        :return:
        """
        return self.driver.execute_script(script, element)


class Wait:
    """ WebdriverWait wrapper """
    TIMEOUT = 60
    FREQ = 0.5

    def __init__(self, driver):
        self.wait = WebDriverWait(driver, timeout=self.TIMEOUT, poll_frequency=self.FREQ)

    def until_clickable(self, locator) -> WebElement:
        """
        :param locator:
        :return: WebElement if element is clickable
        """
        return self.wait.until(ec.element_to_be_clickable(locator))

    def until_presence_of_element(self, locator) -> WebElement:
        """
        :param locator:
        :return: True if element is present
        """
        return self.wait.until(ec.presence_of_element_located(locator))

    def until_visibility_of_element(self, locator) -> WebElement:
        """
        :param locator:
        :return: True if element is visible
        """
        return self.wait.until(ec.visibility_of_element_located(locator))

    def until_visibility_of_all_elements(self, locator) -> list[WebElement]:
        """
        :param locator:
        :return: True if all elements are  visible
        """
        return self.wait.until(ec.visibility_of_all_elements_located(locator))

    def until_presence_of_all_elements(self, locator) -> list[WebElement]:
        """
        :param locator:
        :return: True if elements are present
        """
        return self.wait.until(ec.presence_of_all_elements_located(locator))

    def until_invisibility_of_element(self, locator) -> WebElement | bool:
        """
        :param locator:
        :return: True if element is invisible
        """
        return self.wait.until(ec.invisibility_of_element_located(locator))

    def until_invisibility_of_all_elements(self, locator) -> list[WebElement] | bool:
        """
           :param locator:
           :return: True if all elements are invisible
       """
        return self.wait.until(ec.visibility_of_all_elements_located(locator))
