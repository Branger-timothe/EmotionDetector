import os
import urllib.request

MODEL_PATH = "model/best.pt"
MODEL_URL = "https://github.com/RionDsilvaCS/yolo-hand-pose/raw/main/model/best.pt"

def ensure_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs("model", exist_ok=True)
        print("Downloading model...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Model downloaded.")
