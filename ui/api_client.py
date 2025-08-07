def submit_test_solution(test_id, submission_id, jwt_token, language, code):
    """
    Submits a code solution for a test to the API.

    Args:
        test_id (str): The test ID to submit to.
        submission_id (str): The static submission ID (resource ID).
        jwt_token (str): The JWT token for authentication.
        language (str): The programming language (e.g., 'sql').
        code (str): The code to submit.

    Returns:
        dict or None: The JSON response from the API if successful, otherwise None.
    """
    url = f"https://bytexl.app/api/tests/{test_id}/submit/{submission_id}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "solution": {
            "codingSolution": {
                "language": language,
                "code": code
            }
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"[DEBUG] POST {url} status: {response.status_code}")
        if response.status_code == 200:
            print("[DEBUG] Submission successful!")
            data = response.json()
            print(f"[DEBUG] Response: {data}")
            # Optionally save to file
            try:
                with open('code_submission_response.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("[DEBUG] Saved response to code_submission_response.json")
            except Exception as file_err:
                print(f"[DEBUG] Failed to save code_submission_response.json: {file_err}")
            return data
        else:
            print(f"[DEBUG] API error: {response.text}")
            return None
    except Exception as e:
        print(f"[DEBUG] API call failed: {e}")
        return None
    

    
def print_questions_from_dat_json():
    """Print all question titles and descriptions from dat.json."""
    try:
        with open('dat.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        questions = data.get('data', {}).get('questions', [])
        if not questions:
            print('[DEBUG] No questions found in dat.json')
            return
        print('[DEBUG] Questions in dat.json:')
        for idx, q in enumerate(questions, 1):
            print(f"\nQuestion {idx}:")
            print(f"Title: {q.get('title', '')}")
            print(f"Description: {q.get('description', '')}")
    except Exception as e:
        print(f"[DEBUG] Failed to read or parse dat.json: {e}")
import requests
import json

def fetch_cu_courses(jwt_token):
    API_URL = "https://bytexl.app/api/courses?includeMetrics=true"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    try:
        print(f"[DEBUG] Calling API: {API_URL}")
        print(f"[DEBUG] Headers: {headers}")
        response = requests.get(API_URL, headers=headers)
        print(f"[DEBUG] API GET {API_URL} status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                cu_courses = [course for course in data if str(course.get('title', '')).strip().startswith('CU')]
            elif isinstance(data, dict) and 'courses' in data:
                cu_courses = [course for course in data['courses'] if str(course.get('title', '')).strip().startswith('CU')]
            else:
                cu_courses = []
            return cu_courses
        else:
            print(f"[DEBUG] API error: {response.text}")
            return None
    except Exception as e:
        print(f"[DEBUG] Error fetching courses: {e}")
        return None

def fetch_lab_data(lab_id, jwt_token):
    api_url = f"https://bytexl.app/api/lab/{lab_id}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    try:
        print(f"[DEBUG] Calling API: {api_url}")
        print(f"[DEBUG] Headers: {headers}")
        response = requests.get(api_url, headers=headers)
        print(f"[DEBUG] API GET {api_url} status: {response.status_code}")
        print(f"[DEBUG] Response: {response.text}")
        if response.status_code == 200:
            print("[DEBUG] Lab data fetched successfully.")
            return response.json()
        else:
            print(f"[DEBUG] API error: {response.text}")
            return None
    except Exception as e:
        print(f"[DEBUG] API call failed: {e}")
        return None

def fetch_test_questions(test_id, jwt_token):
    api_url = f"https://bytexl.app/api/tests/{test_id}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    try:
        print(f"[DEBUG] Calling API: {api_url}")
        print(f"[DEBUG] Headers: {headers}")
        response = requests.get(api_url, headers=headers)
        print(f"[DEBUG] API GET {api_url} status: {response.status_code}")
        if response.status_code == 200:
            print("[DEBUG] Test questions fetched successfully.")
            data = response.json()
            print(f"[DEBUG] Response: {data}")
            # Save to dat.json
            try:
                with open('dat.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("[DEBUG] Saved response to dat.json")
            except Exception as file_err:
                print(f"[DEBUG] Failed to save dat.json: {file_err}")
            return data
        else:
            print(f"[DEBUG] API error: {response.text}")
            return None
    except Exception as e:
        print(f"[DEBUG] API call failed: {e}")
        return None
    

