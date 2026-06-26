import json
import sys
from pathlib import Path

def open_json(file_name):
    path = relative_path(file_name)
    with open(path, "r") as file:
        data = json.load(file)
    return data

def load_json(contents):
    return json.loads(contents)

def relative_path(file_name):
    if getattr(sys, "frozen", False):
        # Running as .exe
        base = Path(sys._MEIPASS)
    else:
        # Running as .py
        base = Path(__file__).resolve().parent.parent

    return base / file_name

def save_json(dir, file_name, data):
    path = Path(dir) / file_name
    with open(path, "w") as file:
        json.dump(data, file, indent=4)