from threading import Lock
from app.chatbot.engine import Chatbot
from app.services.storage import Storage

class AppState:
    def __init__(self):
        self.chatbot = Chatbot()
        self.storage = Storage()
        self.lock = Lock()