import cv2
import numpy as np
import pytesseract
from PIL import Image
import io

# ================= TESSERACT PATH (WINDOWS) =================
# ✅ CHANGE only if your path is different
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ================= IMAGE PREPROCESSING =================
def preprocess_image(image):
    """
    Improve image quality for OCR
    """

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise
    gray = cv2.medianBlur(gray, 3)

    # Adaptive threshold (best for mixed lighting)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


# ================= OCR FUNCTION =================
def extract_text_from_image(file):
    """
    Takes FastAPI UploadFile and returns extracted text
    """

    try:
        # Read file bytes
        contents = file.file.read()

        # Convert to numpy array
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_np = np.array(image)

        # Convert RGB -> BGR (OpenCV format)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Preprocess image
        processed = preprocess_image(image_np)

        # ================= TESSERACT CONFIG =================
        custom_config = r'--oem 3 --psm 6'

        text = pytesseract.image_to_string(processed, config=custom_config)

        return text.strip()

    except Exception as e:
        print("OCR ERROR:", e)
        return ""