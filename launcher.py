import uvicorn
import requests
import time
import webview
import threading
from app.main import app
from app.config import WEBVIEW

window = None


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)


def wait_for_server():
    # wait until FastAPI is ready
    for _ in range(50):  # ~10 seconds timeout
        try:
            requests.get("http://127.0.0.1:8000", timeout=1)
            break
        except requests.RequestException:
            time.sleep(0.2)
    else:
        print("Server failed to start")
        return

    # safely update UI on main thread
    if window:
        window.load_url("http://127.0.0.1:8000")


def launch_desktop():
    global window

    threading.Thread(target=run_server, daemon=True).start()

    window = webview.create_window(
        "AI Chatbot",
        html="""
        <html>
        <body style="
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            font-family:Arial;
        ">
            <h2>Loading AI Chatbot...</h2>
        </body>
        </html>
        """,
        width=1600,
        height=900
    )

    threading.Thread(target=wait_for_server, daemon=True).start()

    webview.start()


if __name__ == "__main__":
    if WEBVIEW:
        launch_desktop()
    else:
        run_server()