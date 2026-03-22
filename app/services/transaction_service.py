import pandas as pd

def clean_data(df):
    df.columns = df.columns.str.lower()

    # check required columns
    required_cols = ['date', 'description', 'amount']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # clean amount
    df['amount'] = df['amount'].replace('[₹,]', '', regex=True).astype(float)

    # classify debit/credit
    df['type'] = df['amount'].apply(lambda x: 'debit' if x < 0 else 'credit')

    return df


def process_file(file):
    df = pd.read_csv(file)

    df = clean_data(df)

    return df.to_dict(orient="records")