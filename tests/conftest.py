import pytest
import json
from pytest import StashKey, CollectReport
from typing import Dict

from framework.tests.config import Config
from settings import ROOT_DIR
from framework.reporter import AllureReporter
from framework.web_browser import WebBrowser
from framework.logger import get_logger
from web_pages.terminal_x.terminal_x import TerminalX

logger = get_logger()
phase_report_key = StashKey[Dict[str, CollectReport]]()

ALLURE_RESULTS_PATH = fr'{ROOT_DIR}\allure-results'


@pytest.fixture(scope='function')
def driver(request, browser_type):
    browser = browser_type
    try:
        driver = WebBrowser(browser)
        yield driver
        driver.quit_driver()
    except Exception as e:
        logger.error(e)


@pytest.fixture
def reporter():
    return AllureReporter()


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    # execute all other hooks to obtain the report object
    rep = yield
    # store test results for each phase of a call, which can
    # be "setup", "call", "teardown "
    item.stash.setdefault(phase_report_key, {})[rep.when] = rep
    return rep


@pytest.fixture(autouse=True)
def test_details(driver) -> dict:
    """
    retrieve current driver information
    """
    if driver is None:
        return {
            'name': 'None',
            'version': 'None',
            'platform': 'None'
        }
    return {
        'name': driver.name.capitalize(),
        'version': driver.capabilities['browserVersion'],
        'platform': driver.capabilities['platformName'].capitalize()
    }


@pytest.fixture(autouse=True)
def write_test_details(test_details: dict) -> None:
    """
    Get current driver information and writes it to environment properties file in the allure-results path
    """
    info = f'\nBrowser={test_details["name"]}\nVersion={test_details["version"]}\nPlatform={test_details["platform"]}'
    env_properties_path = fr'{ALLURE_RESULTS_PATH}\environment.properties'
    logger.info(f"path is {env_properties_path}")
    with open(env_properties_path, 'w') as f:
        f.write(info)
    logger.info(f"writing current driver details")


@pytest.fixture(autouse=True, scope="function")
def screenshot_on_failure(request, driver, reporter):
    yield  # Allow the test to run
    report = request.node.stash[phase_report_key]
    if report.get("call").failed or report.get("setup").failed:
        if driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                logger.info("Test failed: attaching screenshot.")
                reporter.attach_img(screenshot=screenshot)
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")
        else:
            logger.info("Test failed: driver is not available, skipping screenshot.")


@pytest.fixture(scope="function")
def terminal_x_ui(driver, app_config, request):
    return TerminalX(driver)


def pytest_addoption(parser):
    parser.addoption("--browser_type", action="store", help="browser for the automation tests", default="chrome")
    parser.addoption("--user", action="store", help="user for swag labs", default="standard")
    parser.addoption("--is_local", action="store", help="run locally or remotely, accept true/false", default=True)
    parser.addoption("--allurdir", action="store", help="allure results directory", default="allure-results")


@pytest.fixture(scope="session")
def user(request):
    return request.config.getoption("--user")


@pytest.fixture(scope='session')
def browser_type(request):
    return request.config.getoption("--browser_type")


@pytest.fixture(scope='session')
def is_local(request):
    return request.config.getoption('--is_local')


@pytest.fixture(scope='session')
def app_config(is_local, browser_type):
    cfg = Config(is_local=is_local,
                 browser_type=browser_type
                 )
    return cfg


def pytest_collection_modifyitems(items):
    test_info = {
        item.nodeid.split("::")[1]: item.function.__doc__
        for item in items
    }
    logger.info('Test information including params:\n{}'.format(json.dumps(test_info, indent=2)))

    for item in items:
        # Check if the test uses the para_bank_api fixture
        if 'pet_store_api' in getattr(item, 'fixturenames', []):
            item.add_marker('api')


@pytest.fixture
def login_data(request):
    user: str = request.param
    with open(fr'{ROOT_DIR}\tests\login_data.json') as json_file:
        return json.load(json_file).get(user)
