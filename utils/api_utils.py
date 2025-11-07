from playwright.sync_api import Playwright

# ------------------------------------------------------
# Static order payload (temporary placeholder)
# Ideally, this should be loaded from an external JSON file
# (e.g., data/order_payload.json) for flexibility.
# ------------------------------------------------------
ordersPayLoad = '{"orders":[{"country":"India","productOrderedId":"68a961459320a140fe1ca57a"}]}'


class APIUtils:
    """
    A utility class that encapsulates all API interactions
    related to user authentication and order creation.

    This layer allows Playwright tests to set up data (like orders)
    quickly via API calls, instead of relying on slow UI workflows.
    """

    def getToken(self, playwright: Playwright, user_credentials):
        """
        Authenticate the user via API and return an access token.

        Args:
            playwright (Playwright): Playwright instance for request context.
            user_credentials (dict): Dictionary containing 'userEmail' and 'userPassword'.

        Returns:
            str: Authentication token to be used in subsequent API calls.
        """
        # Create a fresh request context for API calls.
        api_request_context = playwright.request.new_context(
            base_url="https://rahulshettyacademy.com"
        )

        # Send a POST request to the login endpoint with user credentials.
        response = api_request_context.post(
            "api/ecom/auth/login",
            data={
                "userEmail": user_credentials["userEmail"],
                "userPassword": user_credentials["userPassword"],
            },
            headers={"content-type": "application/json"},
        )

        # Log the response for debugging or reporting.
        print("Login Status:", response.status)
        print("Login Response Body:", response.text())

        # Extract and return the authentication token from the response JSON.
        token = response.json()["token"]
        return token


    def createOrder(self, playwright: Playwright, user_credentials):
        """
        Create a new order using the authenticated API session.

        Args:
            playwright (Playwright): Playwright instance for request context.
            user_credentials (dict): Dictionary containing user login details.

        Returns:
            str: The unique order ID created by the API.
        """
        # Step 1: Retrieve a fresh token for the given user.
        token = self.getToken(playwright, user_credentials)

        # Step 2: Create a new API request context with authorization.
        api_request_context = playwright.request.new_context(
            base_url="https://rahulshettyacademy.com"
        )

        # Step 3: Send a POST request to create an order using the payload.
        response = api_request_context.post(
            "api/ecom/order/create-order",
            data=ordersPayLoad,
            headers={
                "Authorization": token,
                "content-type": "application/json",
            },
        )

        # Log the complete response for debugging purposes.
        print(response.json())

        # Step 4: Extract the order ID from the API response.
        response_body = response.json()
        orderId = response_body["orders"][0]

        # Return the generated order ID for use in UI validation.
        return orderId
