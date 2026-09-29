import requests
# Test after running app.py

base = "http://127.0.0.1:5000"
headers = {"X-API-KEY": "gokula_api_key_2026"}

# Create
r = requests.post(f"{base}/api/students", json={"name":"Gokula","email":"gokula@test.com","course":"Python"}, headers=headers)
print(r.json())
