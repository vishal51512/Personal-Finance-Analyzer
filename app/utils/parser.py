import re
import pandas as pd
import pdfplumber
from docx import Document
from app.utils.format_detector import detect_format
from app.utils.nlp_cleaner import extract_merchant
from app.utils.llm_parser import extract_transactions_llm


# =========================
# 📥 EXTRACT TEXT
# =========================
def extract_text(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        raise ValueError("Unsupported file format")

    return text


# =========================
# 🔍 GPAY PARSER
# =========================
def parse_gpay(text):
    lines = text.split("\n")

    data = []
    current = {}

    for line in lines:
        line = line.strip()

        # date (01 Dec 2025)
        date_match = re.search(r"\d{1,2}\s\w{3}\s\d{4}", line)
        if date_match:
            if current:
                data.append(current)
                current = {}

            current["date"] = date_match.group()

        # description
        if "Paid to" in line or "Received from" in line:
            current["description"] = line

        # amount
        amount_match = re.search(r"₹\s?([\d,]+\.\d+|\d+)", line)
        if amount_match:
            amount = float(amount_match.group(1).replace(",", ""))

            if "paid" in current.get("description", "").lower():
                amount = -amount

            current["amount"] = amount

    if current:
        data.append(current)

    return data


# =========================
# 🧾 PAYTM PARSER
# =========================
def parse_paytm(text):
    # simple reuse (can customize later)
    return parse_gpay(text)


# =========================
# 🏦 BANK PARSER
# =========================
def parse_bank(text):
    # basic parser (can extend)
    return parse_gpay(text)


# =========================
# 🧹 CLEAN DATAFRAME
# =========================
def to_dataframe(data):
    df = pd.DataFrame(data)

    if df.empty:
        return df

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    df = df.dropna(subset=['date', 'amount'])

    # NLP merchant extraction
    df['merchant'] = df['description'].apply(extract_merchant)

    return df


# =========================
# 🤖 MAIN PARSER
# =========================
def parse_file(file_path):
    text = extract_text(file_path)

    format_type = detect_format(text)

    try:
        if format_type == "gpay":
            data = parse_gpay(text)

        elif format_type == "paytm":
            data = parse_paytm(text)

        elif format_type == "bank":
            data = parse_bank(text)

        else:
            data = parse_gpay(text)

        # fallback to LLM if poor extraction
        if len(data) < 5:
            raise Exception("Low extraction")

    except:
        print("⚠️ Using LLM fallback...")
        data = extract_transactions_llm(text)

    df = to_dataframe(data)

    return df