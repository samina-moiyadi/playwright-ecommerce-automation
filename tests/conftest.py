import pytest

# --------------------------------------------------------
# Custom Command-Line Option for Browser Selection
# --------------------------------------------------------
# This hook adds a CLI option (--browser_name) to pytest.
# It allows running tests across different browsers dynamically:
#   pytest --browser_name=firefox
# Default browser: Chrome
# --------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )


# --------------------------------------------------------
# Fixture: user_credentials
# --------------------------------------------------------
# A parameterized fixture that provides user credential data
# when used in combination with @pytest.mark.parametrize(...).
# The request.param attribute contains one set of credentials
# (email, password) for each iteration.
# --------------------------------------------------------
@pytest.fixture(scope='session')
def user_credentials(request):
    return request.param


# --------------------------------------------------------
# Fixture: browserInstance
# --------------------------------------------------------
# Creates and manages a browser instance for each test.
# The browser type (Chrome or Firefox) is determined at runtime
# using the --browser_name CLI option.
#
# Scope: function-level (default) – each test gets a fresh context.
# After the test finishes, the context and browser are properly closed.
# --------------------------------------------------------
@pytest.fixture
def browserInstance(playwright, request):
    # Retrieve the selected browser from command-line options
    browser_name = request.config.getoption("browser_name")

    # Launch browser based on selected option
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Create a new browser context (isolated session)
    context = browser.new_context()

    # Open a fresh page for the test
    page = context.new_page()

    # Yield the page object to the test function
    yield page

    # Teardown: close context and browser after test completion
    context.close()
    browser.close()
