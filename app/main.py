from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.state import AppState
from app.api import routes_ml, routes_chat
from app.services.file_loader import relative_path
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.state = AppState()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_ml.router)
app.include_router(routes_chat.router)

app.mount(
    "/",
    StaticFiles(directory=str(relative_path("static")), html=True),
    name="static"
)