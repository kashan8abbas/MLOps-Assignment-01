import pandas as pd
from app.model_utils import load_model, predict_with_model

model = load_model("models/model.pkl")
df = pd.read_csv("data/dataset_GROUP_DEMO.csv")
X = df.drop(columns=["target"]).head(5).values.tolist()
print(predict_with_model(model, X))
