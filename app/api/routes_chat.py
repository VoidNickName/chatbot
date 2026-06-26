from fastapi import APIRouter, UploadFile, File, Request
from pydantic import BaseModel
from app.utils import errors
from app.chatbot.knowledge import validate_knowledgebase, save_knowledgebase
from app.chatbot.engine import load_knowledgebase, cache_pattern

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/question")
def ask(data: Question, request: Request):

    chatbot = request.app.state.chatbot
    answer, confidence = chatbot.respond(data.question)

    return {
        "answer": answer,
        "confidence": confidence
    }

@router.post("/upload-knowledgebase")
async def upload_knowledgebase(file: UploadFile = File(...), request: Request = None):
    file_name = file.filename
    
    if not file_name or "." not in file_name:
        raise errors.invalid_filename(file_name)

    ext = file_name.rsplit(".", 1)[1].lower()

    if ext not in ["json"]:
        raise errors.invalid_extension(ext)
    
    # Process the uploaded JSON file
    contents = await file.read()
    if validate_knowledgebase(contents):
        save_knowledgebase(contents, file_name)
        load_knowledgebase(request.app.state.chatbot)
        cache_pattern(request.app.state.chatbot)

    return {
        "file_name": file_name
    }