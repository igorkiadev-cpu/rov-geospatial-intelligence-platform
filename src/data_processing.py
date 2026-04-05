def clean_data(df):
    # padroniza nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # possíveis variações
    df = df.rename(columns={
        "lat": "latitude",
        "lon": "longitude",
        "long": "longitude"
    })

    # validação
    required_cols = ["latitude", "longitude", "depth"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Colunas obrigatórias faltando: {missing}")

    # limpa espaços (só string)
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # 🔥 converte para número (ESSENCIAL)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["depth"] = pd.to_numeric(df["depth"], errors="coerce")

    # remove linhas inválidas
    df = df.dropna(subset=["latitude", "longitude", "depth"])

    return df
