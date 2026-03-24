import os
import json

def load_folder(folder_name):
    # Go to app folder
    base_dir = os.path.dirname(os.path.dirname(__file__))  
    # This points to: backend/app/

    folder_path = os.path.join(base_dir, "data", folder_name)

    print("Final path:", folder_path)

    all_data = []

    for file in os.listdir(folder_path):
        if file.endswith(".jsonl"):
            full_path = os.path.join(folder_path, file)

            with open(full_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        all_data.append(json.loads(line))

    return all_data