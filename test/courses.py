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
        # Note: A 304 Not Modified status also indicates a successful check,
        # but the response body will be empty as the content hasn't changed.
        if response.status_code == 200:
            print("Request successful!")
            # Parse and return the JSON response
            return response.json()
        elif response.status_code == 304:
            print(f"Request successful with status code: {response.status_code} (Not Modified)")
            print("The content has not changed since the last request.")
            return None # Or handle as appropriate if you need to know it was 304
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None

def save_json_to_file(data, filename="response.json"):
    """
    Saves a Python dictionary (JSON data) to a specified file.

    Args:
        data (dict): The dictionary to save as JSON.
        filename (str): The name of the file to save to.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except IOError as e:
        print(f"Error saving data to file {filename}: {e}")

# --- Configuration ---
# Replace this with your actual JWT token
YOUR_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0M3FlamRnZXYiLCJlbWFpbCI6IjIzYmNzMTA2NzhAY3VjaGQuaW4iLCJpYXQiOjE3NTQ0MTMzNDd9.uUJYWu_gTpkQKOHh7wWd3gkIlMYfabjKbCjzrrcGWRU"

# The API endpoint you want to access
API_URL = "https://bytexl.app/api/courses?includeMetrics=true"

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
            
            # --- Save data to file ---
            save_json_to_file(data, "courses_data.json")
        else:
            print("\nFailed to retrieve data or content not modified.")

