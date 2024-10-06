# Automation Test Project

This project is designed to automate the testing of the TerminalX web application using Selenium and Pytest. The tests cover various functionalities such as login, search results, and product details.

## Project Structure

- `web_pages/`: Contains page object models for different pages of the TerminalX website.
- `tests/`: Contains test cases and utility functions.
- `framework/`: Contains framework utilities like browser management, reporting, and logging.
- `config/`: Contains configuration files.

## Prerequisites

- Python 3.x
- Pip (Python package installer)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Update the `config/config.json` file with the appropriate settings for your environment.

## Running the Tests

1. To run the tests, use the following command:
    ```sh
    pytest --browser_type=chrome  
    ```

2. To generate an Allure report cd to the test directory and use the following command:
    ```sh
    allure serve allure-results
    ```

## Additional Information

- The tests use the Allure framework for reporting.
- The `tests/conftest.py` file contains fixtures for setting up the test environment.
- The `tests/utils.py` file contains utility functions used in the tests.

## License

This project is licensed under the MIT License.