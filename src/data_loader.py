import pandas as pd

def load_data(file):
    df = pd.read_csv(file)

    # 🔥 Padroniza nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # 🔥 Remove colunas totalmente vazias (às vezes CSV vem quebrado)
    df = df.dropna(axis=1, how='all')

    # 🔥 Colunas obrigatórias
    required_cols = ['latitude', 'longitude', 'depth']

    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # 🔥 Converte tipos (evita bug silencioso)
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['depth'] = pd.to_numeric(df['depth'], errors='coerce')

    # 🔥 Timestamp (se existir)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # 🔥 Boolean de anomalia (se existir)
    if 'anomaly' in df.columns:
        df['anomaly'] = df['anomaly'].astype(str).str.lower().map({
            'true': True,
            'false': False
        })

    # 🔥 Remove linhas inválidas (coordenadas quebradas)
    df = df.dropna(subset=['latitude', 'longitude', 'depth'])

    return df
