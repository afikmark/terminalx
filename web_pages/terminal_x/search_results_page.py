from selenium.webdriver.common.by import By
from framework.ui_elements import Locator, HyperLink, Component
from framework.utils import retry_on_empty_result
from web_pages.page import Page
import re


class ProductItem(Component):
    BOTTOM_SECTION = '.bottom_3-q0'
    PRICE_SELECTOR = '.row_2tcG.bold_2wBM.final-price_8CiX'

    def __init__(self, driver):
        self.driver = driver
        super().__init__('', driver)
        self.link_description = HyperLink(f'.tx-link-a.title_3ZxJ', driver)
        self.price_locator = Locator(By.CSS_SELECTOR, self.PRICE_SELECTOR)

    @property
    @retry_on_empty_result()
    def price(self):
        """Returns the price"""
        price = self.driver.find_element(Locator(By.CSS_SELECTOR, self.PRICE_SELECTOR)).text
        return price.replace('₪', '').strip()


class SearchResults(Page):
    PRICE_SELECTOR = '.row_2tcG.bold_2wBM.final-price_8CiX'

    def __init__(self, driver):
        self.url = 'https://www.terminalx.com/catalogsearch/result/?q='
        super().__init__(driver, self.url)
        self.listing_product = Locator(By.CSS_SELECTOR, '.listing-product_3mjp')
        self.price_locator = Locator(By.CSS_SELECTOR, self.PRICE_SELECTOR)

    def get_all_products(self) -> list:
        """Returns list of all product elements"""
        return self.driver.find_elements(self.listing_product)

    @retry_on_empty_result()
    def get_product_price(self, product):
        """Returns the price"""
        price = product.find_element(By.CSS_SELECTOR, self.PRICE_SELECTOR).text
        return price.replace('₪', '').strip()

    def product_link(self, product):
        """Returns the hyperlink"""
        return product.find_element(By.CSS_SELECTOR, '.tx-link-a.title_3ZxJ')
