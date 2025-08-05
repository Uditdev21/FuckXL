import requests
import json

def make_authenticated_get_request(url, jwt_token):
    """
    Makes a GET request to a specified URL with a JWT token in the Authorization header.

    Args:
        url (str): The URL to send the GET request to.
        jwt_token (str): The JSON Web Token (JWT) for authentication.

    Returns:
        dict or None: The JSON response from the API if successful, otherwise None.
    """
    headers = {
        "Authorization": f"Bearer {jwt_token}", # Standard way to send JWT in headers
        "Content-Type": "application/json"      # Often good practice for API requests
    }

    try:
        # Send the GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful!")
            # Parse and return the JSON response
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None

# --- Configuration ---
# Replace this with your actual JWT token
YOUR_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0M3FlamRnZXYiLCJlbWFpbCI6IjIzYmNzMTA2NzhAY3VjaGQuaW4iLCJpYXQiOjE3NTQ0MTMzNDd9.uUJYWu_gTpkQKOHh7wWd3gkIlMYfabjKbCjzrrcGWRU"

# The API endpoint you want to access
API_URL = "https://bytexl.app/api/courses/with-progress/43qcd2azf"

# --- Execute the request ---
if __name__ == "__main__":
    if YOUR_JWT_TOKEN == "YOUR_JWT_TOKEN_HERE":
        print("WARNING: Please replace 'YOUR_JWT_TOKEN_HERE' with your actual JWT token before running.")
    else:
        print(f"Attempting to fetch data from: {API_URL}")
        data = make_authenticated_get_request(API_URL, YOUR_JWT_TOKEN)

        if data:
            print("\n--- Received Data ---")
            # You can pretty-print the JSON data for better readability
            print(json.dumps(data, indent=4))
        else:
            print("\nFailed to retrieve data.")

