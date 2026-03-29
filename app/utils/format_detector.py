def detect_format(text):
    text = text.lower()

    if "upi transaction id" in text or "google pay" in text:
        return "gpay"

    if "paytm" in text:
        return "paytm"

    if "account statement" in text or "bank" in text:
        return "bank"

    return "unknown"