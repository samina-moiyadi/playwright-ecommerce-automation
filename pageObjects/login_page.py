from pytest_playwright.pytest_playwright import page
from .dashboard_page import DashboardPage

class LoginPage:
    def __init__(self, page):
        # Store the Playwright Page instance for element interactions
        self.page = page

    def navigate(self):
        """
        Navigate to the application's login page.
        """
        self.page.goto("https://rahulshettyacademy.com/client/")

    def login(self, userEmail, userPassword):
        """
        Perform login using provided credentials.
        Returns a DashboardPage object upon successful login.
        """
        # Fill in email and password fields
        self.page.get_by_placeholder("email@example.com").fill(userEmail)
        self.page.get_by_placeholder("enter your passsword").fill(userPassword)

        # Click the Login button
        self.page.get_by_role("button", name="Login").click()

        # Instantiate and return DashboardPage for further navigation
        dashboardPage = DashboardPage(self.page)
        return dashboardPage
