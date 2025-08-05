from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Open the login page
    driver.get("https://bytexl.app")

    print("\n🧠 Do the login manually (fill email, password, CAPTCHA, then click Login).")
    input("➡️  Press ENTER here once you've clicked 'Login'...")

    # Look for the /api/user/signin request
    found = False
    for request in driver.requests:
        if request.method == "POST" and "/api/user/signin" in request.url and request.response:
            found = True
            print("\n✅ Found login request.")
            print(f"URL: {request.url}")
            print(f"Status: {request.response.status_code}")

            # Print response body as JSON
            try:
                body = request.response.body.decode("utf-8")
                json_body = json.loads(body)
                print("\n📥 Response JSON:")
                print(json.dumps(json_body, indent=2))
            except:
                print("\n⚠️ Couldn't decode JSON. Raw body:")
                print(body)

            break

    if not found:
        print("❌ No login API request was captured.")

finally:
    input("\n🔚 Press ENTER to close the browser...")
    driver.quit()
