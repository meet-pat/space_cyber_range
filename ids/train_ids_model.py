import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample training data
commands = [
    "start_camera", "adjust_altitude", "activate_thruster",
    "shutdown_thruster", "calibrate_sensors", "reset_sensors"
]

labels = [0, 0, 0, 0, 0, 0]  # 0 = Normal

# Add some fake/spoofed commands
commands += [
    "self_destruct", "shutdown_comms", "delete_logs", "override_all", "inject_payload"
]
labels += [1, 1, 1, 1, 1]  # 1 = Malicious

# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(commands)
model = LogisticRegression()
model.fit(X, labels)

# Save vectorizer and model
with open("ids/ids_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("[+] IDS Model trained and saved.")
