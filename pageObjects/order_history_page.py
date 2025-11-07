from order_details_page import OrderDetailsPage

class OrderHistoryPage:
    """
    Page Object representing the Order History page of the application.
    Provides methods to interact with orders listed in the user's history.
    """

    def __init__(self, page):
        # Store the Playwright Page instance for UI interactions on this page
        self.page = page

    def selectOrder(self, orderId):
        """
        Select a specific order from the order history table.

        Steps:
        1. Locate the table row containing the given order ID.
        2. Click the 'View' button in that row.
        3. Return the OrderDetailsPage object for further validation.

        Args:
            orderId (str): The unique identifier of the order to open.

        Returns:
            OrderDetailsPage: Page object representing the order details screen.
        """
        # Step 1: Filter the table rows to find the one containing the given orderId
        row = self.page.locator("tr").filter(has_text=orderId)

        # Step 2: Click the 'View' button in the selected row
        row.get_by_role("button", name="View").click()

        # Step 3: Instantiate and return the OrderDetailsPage for further checks
        orderDetailsPage = OrderDetailsPage(self.page)
        return orderDetailsPage
