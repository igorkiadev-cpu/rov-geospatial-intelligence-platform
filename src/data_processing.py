def clean_data(df):
    # padroniza nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # possíveis variações de nome
    df = df.rename(columns={
        "lat": "latitude",
        "lon": "longitude"
    })

    # checagem segura
    required_cols = ["latitude", "longitude", "depth"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória faltando: {col}")

    # limpa dados
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df
