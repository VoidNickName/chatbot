from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def get_model(name):
    if name == "logistic_regression":
        return LogisticRegression()
    elif name == "decision_tree":
        return DecisionTreeClassifier()
    elif name == "random_forest":
        return RandomForestClassifier()
    else:
        raise ValueError("Unknown model")