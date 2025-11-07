from order_history_page import OrderHistoryPage

class DashboardPage:
    def __init__(self, page):
        # Store the Playwright Page instance for UI interactions on the dashboard
        self.page = page

    def selectOrdersNavLink(self):
        """
        Click the 'ORDERS' navigation button on the dashboard
        and return an OrderHistoryPage object for further actions.
        """
        # Click on the 'ORDERS' button to navigate to the order history section
        self.page.get_by_role("button", name="ORDERS").click()

        # Instantiate and return the OrderHistoryPage object
        orderHistoryPage = OrderHistoryPage(self.page)
        return orderHistoryPage
