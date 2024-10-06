from selenium.webdriver.common.by import By

from framework.ui_elements import Locator
from framework.utils import retry_on_empty_result
from web_pages.page import Page


class ProductPage(Page):
    PRICE_SELECTOR = '[data-test-id="qa-pdp-price-final"]'

    def __init__(self, driver):
        self.url = 'https://www.terminalx.com/default-category/'
        super().__init__(driver, self.url)
        self.price_locator = Locator(By.CSS_SELECTOR, self.PRICE_SELECTOR)

    @retry_on_empty_result()
    @property
    def price(self) -> str:
        """Returns the price"""
        price = self.driver.find_element(self.price_locator).text
        return price.replace('₪', '').strip()
