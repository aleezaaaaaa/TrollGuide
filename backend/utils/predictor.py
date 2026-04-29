import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

# ================= LOAD MODEL =================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

# ================= CLEAN =================
def clean_text(text):
    return text.lower().strip()

# ================= RULE BOOST =================
def rule_boost(text):
    strong_words = ["kill", "rape", "murder", "die"]

    for word in strong_words:
        if word in text:
            return "Toxic", 0.99

    return None

# ================= PREDICT =================
def predict(text):
    text = clean_text(text)

    # 🔥 Rule override FIRST
    override = rule_boost(text)
    if override:
        return override

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = F.softmax(outputs.logits, dim=1)

    confidence, pred = torch.max(probs, dim=1)

    pred = pred.item()
    confidence = float(confidence.item())

    # 🔥 Adjust if reversed
    label = "Toxic" if pred == 1 else "Safe"

    return label, confidence

# ================= EXPLAIN =================
def explain(text):
    toxic_words = ["kill", "rape", "hate", "idiot", "stupid"]

    found = [w for w in toxic_words if w in text]

    explanation = (
        f"Toxic due to: {', '.join(found)}"
        if found else "No strong toxic indicators"
    )

    return found, explanation