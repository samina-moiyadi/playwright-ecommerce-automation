import sys
from pathlib import Path
import json

import pytest
from playwright.sync_api import Playwright

from playwright_ecommerce.pageObjects.loginPage import LoginPage
from playwright_ecommerce.utils.apiUtils import APIUtils

# -------------------------------
# Load user credentials from JSON
# -------------------------------
# The credentials are stored externally in a JSON file for easy maintenance
# and data-driven testing of multiple users.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
data_path = BASE_DIR / "playwright_ecommerce" / "data" / "credentials.json"

with open(data_path, "r") as f:
    test_data = json.load(f)
    user_credentials_list = test_data['user_credentials']


# -----------------------------------------------------------
# Test: End-to-End flow combining API and Web UI validation
# -----------------------------------------------------------
# This test:
# 1. Creates an order using API calls (to speed up setup)
# 2. Logs into the web app using UI automation
# 3. Verifies that the newly created order appears in the UI
# -----------------------------------------------------------
@pytest.mark.parametrize('user_credentials', user_credentials_list)
def test_e2e_web_api(playwright: Playwright, browserInstance, user_credentials):

    # --- Extract credentials for the current test user ---
    userEmail = user_credentials['userEmail']
    userPassword = user_credentials['userPassword']

    # --- Step 1: Create order via API ---
    # Uses APIUtils class to authenticate and create an order.
    # This bypasses UI interactions for faster, reliable setup.
    api_utils = APIUtils()
    orderId = api_utils.createOrder(playwright, user_credentials)

    # --- Step 2: Login to application via UI ---
    # Navigates to login page and authenticates with valid credentials.
    loginPage = LoginPage(browserInstance)
    loginPage.navigate()
    dashboardPage = loginPage.login(userEmail, userPassword)

    # --- Step 3: Navigate to Order History ---
    # Opens the Orders section on the dashboard.
    orderHistoryPage = dashboardPage.selectOrdersNavLink()

    # --- Step 4: Open the specific order created via API ---
    # Locates the order using orderId and navigates to its details.
    orderDetailsPage = orderHistoryPage.selectOrder(orderId)

    # --- Step 5: Verify order confirmation message ---
    # Validates that the order details page shows correct confirmation text.
    orderDetailsPage.verifyOrderMessage()