def get_legal_advice(text):
    text = text.lower()

    if "kill" in text or "murder" in text:
        return {
            "crime": "Criminal Intimidation",
            "law": "IPC 503 / 506",
            "actions": [
                "File FIR at nearest police station",
                "Preserve screenshots as evidence",
                "Report online at https://cybercrime.gov.in/"
            ],
            "report_link": "https://cybercrime.gov.in/"
        }

    elif "rape" in text or "sexual" in text:
        return {
            "crime": "Sexual Harassment",
            "law": "IPC 354A / 509",
            "actions": [
                "Immediate FIR",
                "Contact women helpline",
                "Report online at https://cybercrime.gov.in/"
            ],
            "report_link": "https://cybercrime.gov.in/"
        }

    elif "idiot" in text or "hate" in text:
        return {
            "crime": "Online Abuse",
            "law": "IT Act 66 / 67",
            "actions": [
                "Block/report the user",
                "Save evidence",
                "Report online at https://cybercrime.gov.in/"
            ],
            "report_link": "https://cybercrime.gov.in/"
        }

    return {
        "crime": "Safe",
        "law": "No violation",
        "actions": ["No legal action needed"],
        "report_link": None
    }