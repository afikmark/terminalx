from framework.utils import retry_on_empty_result
from web_pages.page import Page
from web_pages.terminal_x import HomePage, SearchResults, ProductPage


class TerminalX(Page):

    def __init__(self, driver):
        self.url = "https://www.terminalx.com/"
        super().__init__(driver, self.url)
        self.home_page = HomePage(driver)
        self.search_results_page = SearchResults(driver)
        self.product_page = ProductPage(driver)

    @retry_on_empty_result()
    def get_login_profile_name(self) -> str:
        """Returns the login profile name"""
        return self.driver.find_element(self.login_profile_locator).text
