from fastapi import HTTPException


# ---------------------------
# File / upload errors
# ---------------------------

def invalid_filename(file_name: str):
    return HTTPException(
        status_code=400,
        detail=f"Invalid filename: {file_name}"
    )


def invalid_extension(ext: str):
    return HTTPException(
        status_code=400,
        detail=f"Invalid extension: {ext}"
    )


def file_not_found(file_name: str):
    return HTTPException(
        status_code=404,
        detail=f"File not found: {file_name}"
    )


# ---------------------------
# Dataset / feature errors
# ---------------------------

def feature_not_found(feature: str):
    return HTTPException(
        status_code=404,
        detail=f"{feature} not found"
    )


def target_not_found(target: str):
    return HTTPException(
        status_code=404,
        detail=f"{target} not found"
    )


def target_in_features():
    return HTTPException(
        status_code=400,
        detail="Target column cannot be included in features"
    )


# ---------------------------
# Validation errors
# ---------------------------

def invalid_train_test_split():
    return HTTPException(
        status_code=400,
        detail="Train size and test size must be between 0 and 100 and add up to 100"
    )