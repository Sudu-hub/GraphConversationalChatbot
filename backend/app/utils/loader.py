import os
import json
import pandas as pd

def load_folder(folder_name):
    base_dir = os.path.dirname(os.path.dirname(__file__))  
    folder_path = os.path.join(base_dir, "data", folder_name)

    print("Loading from:", folder_path)

    all_data = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"{folder_path} does not exist")

    for file in os.listdir(folder_path):
        if file.endswith(".jsonl"):
            full_path = os.path.join(folder_path, file)

            with open(full_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        all_data.append(json.loads(line))

    # ✅ Convert to DataFrame
    df = pd.DataFrame(all_data)

    print(f"{folder_name} loaded: {df.shape}")

    return df