import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from shared import config
from shared.crypto_utils import decrypt_command
import pickle

# Load IDS model
with open("ids/ids_model.pkl", "rb") as f:
    vectorizer, ids_model = pickle.load(f)

def is_malicious(command):
    X_test = vectorizer.transform([command])
    prediction = ids_model.predict(X_test)
    return prediction[0] == 1  # 1 = malicious

app = Flask(__name__)
telemetry_log = []

@app.route("/receive-command", methods=["POST"])
def receive_command():
    data = request.json
    iv = data.get("iv")
    ciphertext = data.get("ciphertext")
    token = data.get("auth_token")

    # Step 1: Token check
    if token != config.AUTH_TOKEN:
        msg = "[SATELLITE] ❌ Unauthorized command attempt blocked."
        telemetry_log.append(msg)
        print(msg)
        return jsonify({"error": "Unauthorized"}), 403

    # Step 2: Decrypt
    decrypted_command = decrypt_command(iv, ciphertext)
    if not decrypted_command:
        msg = "[SATELLITE] 🔐 Failed to decrypt command."
        telemetry_log.append(msg)
        print(msg)
        return jsonify({"error": "Decryption failed"}), 400

    # Step 3: IDS check
    if is_malicious(decrypted_command):
        msg = f"[SATELLITE] 🚨 Malicious command detected: {decrypted_command}"
        telemetry_log.append(f"[ALERT] Blocked malicious command: {decrypted_command}")
        print(msg)
        return jsonify({"error": "Command flagged as malicious"}), 403

    # Step 4: Execute
    log_entry = f"[SATELLITE] ✅ Executing: {decrypted_command}"
    telemetry_log.append(log_entry)
    print(log_entry)
    return jsonify({"status": "executed", "command": decrypted_command})

@app.route("/telemetry", methods=["GET"])
def get_telemetry():
    return jsonify({"telemetry": telemetry_log})

if __name__ == "__main__":
    app.run(host=config.SATELLITE_HOST, port=config.SATELLITE_PORT)
