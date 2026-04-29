def get_legal(pred, text):
    text = text.lower()

    if pred == 1:
        if "kill" in text or "murder" in text:
            return {"type": "threat", "law": "IPC 503", "advice": "Report to police"}
        else:
            return {"type": "toxic", "law": "IPC 504", "advice": "File complaint"}

    return {"type": "neutral", "law": "None", "advice": "No action"}