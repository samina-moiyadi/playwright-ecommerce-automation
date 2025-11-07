from playwright.sync_api import expect

class OrderDetailsPage:
    def __init__(self, page):
        # Store the Playwright Page instance for element interactions
        self.page = page

    def verifyOrderMessage(self):
        """
        Verify that the confirmation message appears on the order details page
        after a successful purchase.
        """
        # Assert that the page contains the expected success message
        expect(self.page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")
