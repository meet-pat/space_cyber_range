import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from shared import config
from shared.crypto_utils import encrypt_command

def send_command(command):
    url = f"http://{config.SATELLITE_HOST}:{config.SATELLITE_PORT}/receive-command"
    encrypted = encrypt_command(command)
    payload = {
        "iv": encrypted["iv"],
        "ciphertext": encrypted["ciphertext"],
        "auth_token": config.AUTH_TOKEN
    }
    response = requests.post(url, json=payload)
    return response.json()

def fetch_telemetry():
    url = f"http://{config.SATELLITE_HOST}:{config.SATELLITE_PORT}/telemetry"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    while True:
        print("\n1. Send Command")
        print("2. Get Telemetry")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            cmd = input("Enter command for satellite: ")
            print(send_command(cmd))
        elif choice == "2":
            print(fetch_telemetry())
        elif choice == "3":
            break
