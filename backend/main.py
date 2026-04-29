from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Troll Guide API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict():
    return {
        "label": "Toxic",
        "confidence": 0.95
    }
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, status
# from fastapi.responses import FileResponse
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from collections import Counter
# import secrets

# # ✅ CLEAN IMPORTS
# from utils.ocr import extract_text_from_image
# from utils.predictor import predict, explain, clean_text, rule_boost
# from utils.pdf import generate_pdf

# from models import Base, Analysis
# from database import SessionLocal, engine
# from model_loader import predict_toxicity

# app = FastAPI()
# security = HTTPBasic()

# Base.metadata.create_all(bind=engine)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# ADMIN_USERNAME = "admin"
# ADMIN_PASSWORD = "1234"

# def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
#     if not (
#         secrets.compare_digest(credentials.username, ADMIN_USERNAME) and
#         secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid admin credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username


# def format_response(label="Safe", confidence=0.0, legal=None):
#     return {
#         "label": label,
#         "confidence": float(confidence) if confidence is not None else 0.5,
#         "legal": legal
#     }

# class TextInput(BaseModel):
#     text: str

# def get_legal_advice(text):
#     text = text.lower()

#     if "kill" in text or "murder" in text:
#         return {
#             "crime": "Criminal Intimidation",
#             "law": "IPC 503 / 506",
#             "actions": ["File FIR", "Report on cybercrime.gov.in", "Preserve screenshots"]
#         }

#     elif "rape" in text or "sexual" in text:
#         return {
#             "crime": "Sexual Harassment",
#             "law": "IPC 354A / 509",
#             "actions": ["Immediate FIR", "Contact helpline", "Submit evidence"]
#         }

#     elif "idiot" in text or "hate" in text:
#         return {
#             "crime": "Online Abuse",
#             "law": "IT Act 66 / 67",
#             "actions": ["Report account", "Block user"]
#         }

#     return {
#         "crime": "Safe",
#         "law": "No violation",
#         "actions": ["No legal action needed"]
#     }


# @app.post("/analyze-all")
# async def analyze_all(text: str = Form(None), file: UploadFile = File(None)):
#     db = SessionLocal()

#     try:
#         extracted_text = ""

#         if file:
#             extracted_text = extract_text_from_image(file)

#         final_text = (text or "") + " " + (extracted_text or "")

#         if not final_text.strip():
#             raise HTTPException(status_code=400, detail="No input provided")

#         final_text = clean_text(final_text)

#         override = rule_boost(final_text)

#         if override:
#             label, confidence = override
#         else:
#             label, confidence = predict(final_text)

#         confidence = confidence if confidence is not None else 0.5

#         keywords, explanation = explain(final_text)
#         legal = get_legal_advice(final_text)

#         new_entry = Analysis(
#             text=text,
#             extracted_text=extracted_text,
#             label=label,
#             confidence=float(confidence),
#             keywords=", ".join(keywords),
#             explanation=explanation,
#             crime=legal.get("crime"),
#             law=legal.get("law")
#         )

#         db.add(new_entry)
#         db.commit()

#         return {
#             "label": label,
#             "confidence": float(confidence),
#             "text": final_text,
#             "extracted_text": extracted_text,
#             "keywords": keywords,
#             "explanation": explanation,
#             "legal": legal
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         db.close()


# @app.post("/analyze")
# async def analyze_text(data: dict):
#     text = data.get("text", "").strip()

#     if not text:
#         return format_response()

    
#     text = clean_text(text)

#     override = rule_boost(text)
#     if override:
#         label, confidence = override
#     else:
#         label, confidence = predict(text)

#     confidence = confidence if confidence is not None else 0.5

#     legal = None
#     if label == "Toxic":
#         legal = {
#             "crime": "Cyberbullying / Online Harassment",
#             "law": "IT Act Section 66A / IPC 507",
#             "actions": [
#                 "Take screenshots",
#                 "Report the user",
#                 "File complaint on cybercrime portal"
#             ]
#         }

#     return format_response(label, confidence, legal)


# @app.post("/image")
# async def analyze_image(file: UploadFile = File(...)):
#     try:
#         text = extract_text_from_image(file)
#         print("OCR TEXT:", text)

#         if not text.strip():
#             return format_response()

#         text = clean_text(text)

#         override = rule_boost(text)
#         if override:
#             label, confidence = override
#         else:
#             label, confidence = predict(text)

#         confidence = confidence if confidence is not None else 0.5

#         legal = None
#         if label == "Toxic":
#             legal = {
#                 "crime": "Cyberbullying via image",
#                 "law": "IT Act + IPC provisions",
#                 "actions": [
#                     "Save the image",
#                     "Report the account",
#                     "File complaint online"
#                 ]
#             }

#         return format_response(label, confidence, legal)

#     except Exception as e:
#         print("IMAGE ERROR:", e)
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/dashboard")
# def get_dashboard():
#     db: Session = SessionLocal()
#     data = db.query(Analysis).all()

#     total = len(data)
#     label_count = Counter([d.label for d in data])
#     crime_count = Counter([d.crime for d in data])

#     db.close()

#     return {
#         "total": total,
#         "safe": label_count.get("Safe", 0),
#         "toxic": label_count.get("Toxic", 0),
#         "crime_distribution": dict(crime_count)
#     }


# @app.get("/records")
# def get_records():
#     db = SessionLocal()
#     data = db.query(Analysis).all()
#     db.close()
#     return data


# @app.get("/history")
# def get_history():
#     db = SessionLocal()
#     data = db.query(Analysis).all()
#     db.close()

#     return [
#         {
#             "text": d.text,
#             "label": d.label,
#             "confidence": d.confidence,
#             "crime": d.crime,
#             "law": d.law
#         }
#         for d in data
#     ]

# @app.get("/admin/records")
# def get_all_records(admin: str = Depends(verify_admin)):
#     db = SessionLocal()
#     data = db.query(Analysis).all()
#     db.close()
#     return data

# @app.delete("/admin/delete/{id}")
# def delete_record(id: int, admin: str = Depends(verify_admin)):
#     db = SessionLocal()

#     record = db.query(Analysis).filter(Analysis.id == id).first()

#     if not record:
#         db.close()
#         raise HTTPException(status_code=404, detail="Record not found")

#     db.delete(record)
#     db.commit()
#     db.close()

#     return {"message": "Deleted successfully"}

# @app.get("/admin/search")
# def search_records(query: str, admin: str = Depends(verify_admin)):
#     db = SessionLocal()
#     results = db.query(Analysis).filter(Analysis.text.contains(query)).all()
#     db.close()
#     return results


# @app.post("/report")
# def report(data: dict):
#     try:
#         file_path = "report.pdf"
#         generate_pdf(data, file_path)

#         return FileResponse(
#             file_path,
#             media_type="application/pdf",
#             filename="report.pdf"
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))