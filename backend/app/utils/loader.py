import json
import glob

def load_json_folder(path):
    data = []
    for file in glob.glob(path + "/*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data.extend(json.load(f))
    return data