import pandas as pd

def clean_data(df):
    for col in ["latitude", "longitude", "depth"]:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["latitude", "longitude", "depth"])

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values("timestamp")

    return df
