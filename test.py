import requests

API_KEY = "AIzaSyD48JR8KHY9HoO_NGSVjo5lfDRT8kfrQ6o"  # Replace with your actual key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText"

payload = {
    "contents": [{"parts": [{"text": "AI in research"}]}]  # Corrected request format
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload, headers=headers)

try:
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())  # Print actual response
except requests.exceptions.JSONDecodeError:
    print("Error: Response is not valid JSON. Raw response:", response.text)
