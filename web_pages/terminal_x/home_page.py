from framework.utils import retry_on_empty_result
from web_pages.page import Page
from framework.ui_elements import Component, Locator, TextInput, Button
from selenium.webdriver.common.by import By


class Modal(Component):
    BASE_SELECTOR = '.swipeable-modal_1f3c'

    def __init__(self, driver):
        self.driver = driver
        super().__init__(self.BASE_SELECTOR, driver, by=By.CSS_SELECTOR)
        self.close_button_locator = Locator(By.CSS_SELECTOR,
                                            f'{self.BASE_SELECTOR} .style-defaults_2iuF.close-btn_3jxl')

    def close_modal(self) -> None:
        """Closes the modal"""
        self.driver.find_element(self.close_button_locator).click()


class LoginDialog(Component):
    BASE_SELECTOR = '.swipeable-modal_1f3c .login-wrapper_3ltC'
    BOTTOM_SECTION_SELECTOR = '.bottom-section_1Ul_'

    def __init__(self, driver):
        super().__init__(self.BASE_SELECTOR, driver)
        self.email_input = TextInput(f'{self.BASE_SELECTOR} {self.BOTTOM_SECTION_SELECTOR} #qa-login-email-input',
                                     driver, By.CSS_SELECTOR)
        self.password_input = TextInput(f'{self.BASE_SELECTOR} {self.BOTTOM_SECTION_SELECTOR} #qa-login-password-input',
                                        driver, By.CSS_SELECTOR)
        self.login_button = Button(
            f'{self.BASE_SELECTOR} {self.BOTTOM_SECTION_SELECTOR} [data-test-id="qa-login-submit"]', driver,
            By.CSS_SELECTOR)

    def login_with_email(self, email: str, password: str) -> None:
        self.email_input.enter_text(email)
        self.password_input.enter_text(password)
        self.login_button.click()


class HomePage(Page):

    def __init__(self, driver):
        self.url = "https://www.terminalx.com/"
        super().__init__(driver, self.url)
        self.login_dialog = LoginDialog(driver)
        self.search_button = Button('[data-test-id="qa-header-search-button"]', driver, by=By.CSS_SELECTOR)
        self.search_input = TextInput('[data-test-id="qa-search-box-input"]', driver, by=By.CSS_SELECTOR)
        self.login_button = Button('[data-test-id="qa-header-login-button"]', driver, by=By.CSS_SELECTOR)
        self.login_profile_locator = Locator(By.CSS_SELECTOR, '.profile_lLJx.rtl_38tZ')

    @retry_on_empty_result()
    def get_login_profile_name(self) -> str:
        """Returns the login profile name"""
        return self.driver.find_element(self.login_profile_locator).text
