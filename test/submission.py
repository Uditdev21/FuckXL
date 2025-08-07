import requests
import json
import re # Import the regular expression module

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
YOUR_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0M3FlamRnZXYiLCJlbWFpbCI6IjIzYmNzMTA2NzhAY3VjaGQuaW4iLCJpYXQiOjE3NTQ0NTk3NTJ9.OXlVteIjqmWeRfRtvZk_jyr3Y4xJExiGpGHWYS2SPmk"

# The API endpoint for lab data (this will be called first)
LAB_API_URL = "https://bytexl.app/api/lab/43qnf5nk3"

# Base URL for tests data (the ID will be appended dynamically)
TESTS_API_BASE_URL = "https://bytexl.app/api/tests/"

# --- Execute the requests ---
if __name__ == "__main__":
    if YOUR_JWT_TOKEN == "YOUR_JWT_TOKEN_HERE":
        print("WARNING: Please replace 'YOUR_JWT_TOKEN_HERE' with your actual JWT token before running.")
    else:
        # --- Fetch and save Lab data ---
        print(f"\n--- Attempting to fetch Lab data from: {LAB_API_URL} ---")
        lab_data = make_authenticated_get_request(LAB_API_URL, YOUR_JWT_TOKEN)

        if lab_data:
            print("\n--- Received Lab Data ---")
            print(json.dumps(lab_data, indent=4))
            save_json_to_file(lab_data, "lab_data.json")

            # --- Extract test ID from lab_data link ---
            test_id = None
            if "link" in lab_data and isinstance(lab_data["link"], str):
                # Use regex to find the ID between /test/ and the next /
                match = re.search(r'/test/([a-zA-Z0-9]+)/', lab_data["link"])
                if match:
                    test_id = match.group(1)
                    print(f"\nExtracted Test ID: {test_id}")
                else:
                    print(f"Could not extract test ID from link: {lab_data['link']}")
            else:
                print("Lab data does not contain a 'link' field or it's not a string.")

            # --- Fetch and save Tests data using the extracted ID ---
            if test_id:
                dynamic_tests_api_url = f"{TESTS_API_BASE_URL}{test_id}"
                print(f"\n--- Attempting to fetch Tests data from: {dynamic_tests_api_url} ---")
                tests_data = make_authenticated_get_request(dynamic_tests_api_url, YOUR_JWT_TOKEN)

                if tests_data:
                    print("\n--- Received Tests Data ---")
                    print(json.dumps(tests_data, indent=4))
                    save_json_to_file(tests_data, "tests_data.json")
                else:
                    print("\nFailed to retrieve Tests data or content not modified.")
            else:
                print("\nSkipping Tests data fetch as no test ID was extracted.")
        else:
            print("\nFailed to retrieve Lab data or content not modified. Cannot proceed to fetch Tests data.")

