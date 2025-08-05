import os
import json

def save_user_data(name, clean_date):
    os.makedirs("JSON_files", exist_ok=True)  # Make sure folder exists
    user_data = {"name": name, "clean_date": clean_date}
    with open("JSON_files/user_data.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f)

def load_user_data():
    try:
        with open("JSON_files/user_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}

