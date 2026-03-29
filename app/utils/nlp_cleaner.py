import re

MERCHANT_MAP = {
    "swiggy": "Food",
    "zomato": "Food",
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "uber": "Travel",
    "ola": "Travel",
    "netflix": "Entertainment",
    "irctc": "Travel",
}


def normalize_description(desc):
    desc = str(desc).lower()

    desc = re.sub(r'\b\d{10,}\b', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()

    return desc


def extract_merchant(desc):
    desc = normalize_description(desc)

    for key in MERCHANT_MAP:
        if key in desc:
            return key.capitalize()

    if "paid to" in desc or "received from" in desc:
        return "Person"

    return "Other"