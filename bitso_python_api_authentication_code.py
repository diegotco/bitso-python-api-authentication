import hmac
import hashlib
import time
import requests

# Replace these with your actual Bitso API Key and Secret
# This is only for testing purposes, for production use the .env file to fetch the API Keys.
API_KEY = "XXXX"
API_SECRET = "XXXXX"

# Base URL and endpoint
BASE_URL = 'https://api-stage.bitso.com/'  # Use https://api.bitso.com/ for production
endpoint = 'api/v3/balance?currency=btc'
method = "GET"

def sign_request(api_key, api_secret, method, endpoint):
    """
    Generate the authorization headers for a Bitso API request.
    """
    # Generate a nonce using the current time in milliseconds
    nonce = str(time.time_ns() // 1_000_000)
    print("Nonce:", nonce)
    
    # Prepare the data string for signing
    data = f"{nonce}{method}{endpoint}"
    print("Data to Sign:", data)
    
    # Generate the HMAC-SHA256 signature
    signature = hmac.new(
        api_secret.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    print("Signature:", signature)
    
    # Return the Authorization header
    authorization = f"Bitso {api_key}:{nonce}:{signature}"
    return {"Authorization": authorization}

# Generate headers
headers = sign_request(API_KEY, API_SECRET, method, f"/{endpoint}")
print("Headers:", headers)

# Full URL for the request
url = f"{BASE_URL}{endpoint}"

# Make the GET request
response = requests.get(url, headers=headers)

# Print the response status and details
print("Status Code:", response.status_code)
if response.status_code == 200:
    try:
        # Decode the JSON response
        response_json = response.json()
        print("Response JSON:", response_json)

        # Process the payload if the request was successful
        if response_json.get("success") and "payload" in response_json:
            balances = response_json["payload"].get("balances", [])
            if balances:
                print("Balances:")
                for index, balance in enumerate(balances):
                    print(f"Balance {index + 1}: {balance}")
            else:
                print("No balances found in the payload.")
        else:
            print("Unexpected response format:", response_json)
    except requests.exceptions.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
else:
    print("Error occurred:", response.text)
