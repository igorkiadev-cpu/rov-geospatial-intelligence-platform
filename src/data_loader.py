import pandas as pd

def load_data(file):
    # 🔥 AUTO-DETECTA separador (resolve 90% dos erros)
    df = pd.read_csv(file, sep=None, engine='python')

    # 🔥 Padroniza nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # 🔥 Remove colunas vazias
    df = df.dropna(axis=1, how='all')

    # 🧪 DEBUG (pode comentar depois)
    print("Colunas detectadas:", df.columns.tolist())

    # 🔥 Se ainda veio tudo em uma coluna (CSV quebrado)
    if len(df.columns) == 1:
        df = pd.read_csv(file, sep=',')
        df.columns = df.columns.str.strip().str.lower()

    # 🔥 Colunas obrigatórias
    required_cols = ['latitude', 'longitude', 'depth']

    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # 🔥 Converte tipos
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['depth'] = pd.to_numeric(df['depth'], errors='coerce')

    # 🔥 Timestamp (se existir)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # 🔥 Boolean de anomalia (se existir)
    if 'anomaly' in df.columns:
        df['anomaly'] = (
            df['anomaly']
            .astype(str)
            .str.strip()
            .str.lower()
            .map({'true': True, 'false': False})
        )

    # 🔥 Remove linhas inválidas
    df = df.dropna(subset=['latitude', 'longitude', 'depth'])

    return df
