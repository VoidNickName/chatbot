from fastapi import APIRouter, UploadFile, File, Request
from pydantic import BaseModel
import pandas as pd
import io
import uuid
from app.ml.trainer import train_test_model
from app.utils import errors

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), request: Request = None):
    file_name = file.filename
    
    if not file_name or "." not in file_name:
        raise errors.invalid_filename(file_name)

    ext = file_name.rsplit(".", 1)[1].lower()

    if ext not in ["csv"]:
        raise errors.invalid_extension(ext)
    
    # Process the uploaded CSV file
    contents = await file.read()
    
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # create an ID
    file_id = str(uuid.uuid4())

    # store DataFrame in memory
    request.app.state.storage.set(file_id, df)

    # extract column names
    columns = df.columns.tolist()

    return {
        "file_id": file_id,
        "file_name": file_name,
        "columns": columns
    }

# Define expected data format
class Payload(BaseModel):
    file_id: str
    model: str
    train_size: float
    test_size: float
    features: list
    target: str

@router.post("/train-test")
def receive_data(payload: Payload, request: Request):
    df = request.app.state.storage.get(payload.file_id)
    if df is None:
        raise errors.file_not_found(payload.file_id)
    
    result = train_test_model(df, payload.model, payload.train_size, payload.test_size, payload.features, payload.target)

    return {
        "test_results": result
    }