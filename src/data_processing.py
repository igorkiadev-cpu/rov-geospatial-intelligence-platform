import pandas as pd

def clean_data(df):
    # padroniza colunas
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "lat": "latitude",
        "lon": "longitude",
        "long": "longitude"
    })

    required = ["latitude", "longitude", "depth"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # limpeza
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # conversão numérica
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["depth"] = pd.to_numeric(df["depth"], errors="coerce")

    # timestamp (se existir)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values("timestamp")

    # remove lixo
    df = df.dropna(subset=["latitude", "longitude", "depth"])

    return df
