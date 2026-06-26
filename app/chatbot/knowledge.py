from app.services.file_loader import open_json, save_json, load_json
from app.config import DATA_DIR

def loading_intents():
    intents = {}

    for file_path in DATA_DIR.iterdir():
        if file_path.is_file():
            data = open_json(file_path)
            for intent in data["intents"]:
                for pattern in intent["patterns"]:
                    intents[pattern] = intent["response"]

    return intents

def validate_knowledgebase(contents):
    data = load_json(contents)
    if not isinstance(data, dict):
        return False

    if "intents" not in data or not isinstance(data["intents"], list):
        return False

    for intent in data["intents"]:
        if not isinstance(intent, dict):
            return False
        if "patterns" not in intent or "response" not in intent:
            return False
        if not isinstance(intent["patterns"], list):
            return False
        if not isinstance(intent["response"], str):
            return False

    return True

def save_knowledgebase(contents, file_name):
    data = load_json(contents)
    save_json(DATA_DIR, file_name, data)