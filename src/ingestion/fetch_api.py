import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Get API key
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

# API URL
url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}"

# Request
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Success!")
    print(data)
else:
    print("Error:", response.status_code)
