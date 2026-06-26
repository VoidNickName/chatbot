from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from app.ml.models import get_model
from app.utils import errors
import pandas as pd

def train_test_model(df, model_name, training_size, testing_size, features, target):    
    for feature in features:
        if feature not in df.columns:
            raise errors.feature_not_found(feature)
        
    if target not in df.columns:
        raise errors.target_not_found(target)
    
    if (
        training_size + testing_size != 100
        or not (0 < training_size < 100)
        or not (0 < testing_size < 100)
    ):
        raise errors.invalid_train_test_split()
    
    if target in features:
        raise errors.target_in_features()
    
    df = factorize_values(df)

    x = df[features]
    y = df[target]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        train_size=training_size/100,
        test_size=testing_size/100,
        random_state=42
    )

    model = get_model(model_name)
    model.fit(x_train, y_train)
    
    predictions = model.predict(x_test)

    return {
        "accuracy": round(accuracy_score(y_test, predictions), 2),
        "precision": round(precision_score(y_test, predictions, average="weighted"), 2),
        "recall": round(recall_score(y_test, predictions, average="weighted"), 2),
        "f1_score": round(f1_score(y_test, predictions, average="weighted"), 2)
    }

def factorize_values(df):
    df = df.copy()

    object_columns = df.select_dtypes(include=["object", "string"]).columns
    df[object_columns] = df[object_columns].apply(lambda s: pd.factorize(s)[0])
    return df