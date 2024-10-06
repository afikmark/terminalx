import time
import pytest
from assertpy import assert_that, soft_assertions

from tests.utils import get_root_font_size, px_to_rem


@pytest.mark.parametrize('login_data', ['first_user', 'second_user'], indirect=True)
def test_login(terminal_x_ui, app_config, login_data, reporter):
    home_page = terminal_x_ui.home_page
    reporter.step("Step", "Open TerminalX home page")
    home_page.open()

    reporter.step("Step", "Wait for login button to be present")
    terminal_x_ui.driver.wait.until_presence_of_element(home_page.login_button._locator)

    reporter.step("Step", "Click on login button")
    home_page.login_button.click()

    reporter.step("Step", "Wait for login dialog to be visible")
    terminal_x_ui.driver.wait.until_visibility_of_element(home_page.login_dialog.login_button._locator)

    user_email = login_data.get('email')
    user_password = login_data.get('password')
    user_name = login_data.get('name')
    reporter.step("Step", "Login with email")
    home_page.login_dialog.login_with_email(user_email,user_password)

    reporter.step("Step", "Wait for login dialog to disappear")
    terminal_x_ui.driver.wait.until_invisibility_of_element(home_page.login_dialog._locator)

    reporter.step("Step", "Assert profile name contains 'checker'")
    assert_that(home_page.get_login_profile_name(), 'profile name').contains(user_name)


def test_search_results(terminal_x_ui, reporter):
    home_page = terminal_x_ui.home_page
    reporter.step("Step", "Open TerminalX home page")
    home_page.open()

    reporter.step("Step", "Wait for search button to be present")
    terminal_x_ui.driver.wait.until_presence_of_element(home_page.search_button._locator)

    reporter.step("Step", "Click on search button")
    home_page.search_button.click()

    reporter.step("Step", "Enter text 'Hello' in search input")
    home_page.search_input.enter_text("Hello")

    reporter.step("Step", "Press enter to search")
    terminal_x_ui.driver.actions.press_enter()

    reporter.step("Step", "Wait for search results to be present")
    terminal_x_ui.driver.wait.until_presence_of_element(terminal_x_ui.search_results_page.listing_product)

    reporter.step("Step", "Get all products from search results")
    products = terminal_x_ui.search_results_page.get_all_products()

    with soft_assertions():
        reporter.step("Step", "Assert each product contains 'Hello Kitty' in the description")
        for product in products:
            assert_that(terminal_x_ui.search_results_page.product_link(product).text).contains("Hello Kitty")

        reporter.step("Step", "Assert third product price is not None")
        third_product = products[2]
        assert_that(terminal_x_ui.search_results_page.get_product_price(third_product)).is_not_none()

        reporter.step("Step", "Get and sort product prices")
        products_prices = [float(terminal_x_ui.search_results_page.get_product_price(product)) for product in products]
        sorted_prices = sorted(products_prices)
        assert_that(products_prices).is_equal_to(sorted_prices)

        reporter.step("Step", "Click on third product link")
        third_product_link = terminal_x_ui.search_results_page.product_link(third_product)
        third_product_link.click()
        time.sleep(.9)

        reporter.step("Step", "Get price element and root font size")
        price_element = terminal_x_ui.driver.find_element(terminal_x_ui.product_page.price_locator)
        root_font_size = get_root_font_size(terminal_x_ui)

        reporter.step("Step", "Get font size in pixels and convert to rem")
        font_size_px = price_element.value_of_css_property('font-size')
        font_size_px = float(font_size_px.replace('px', ''))
        font_size_rem = px_to_rem(font_size_px, root_font_size)

        reporter.step("Step", "Assert font size in rem is 1.8")
        assert_that(font_size_rem).is_equal_to(1.8)
