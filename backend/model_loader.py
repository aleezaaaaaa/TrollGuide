import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 🔥 Path to your model folder
MODEL_PATH = "model"

# ✅ Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# ✅ Load model (supports .safetensors)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# ✅ Set eval mode
model.eval()


def predict_toxicity(text: str):
    try:
        # Tokenize input
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        # Get model output
        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits

        # Convert to probabilities
        probs = torch.softmax(logits, dim=1)

        confidence, predicted_class = torch.max(probs, dim=1)

        confidence = confidence.item()
        predicted_class = predicted_class.item()

        # ✅ Adjust label mapping if needed
        label = "Toxic" if predicted_class == 1 else "Safe"

        return label, confidence

    except Exception as e:
        print("MODEL ERROR:", e)
        return "Safe", 0.5