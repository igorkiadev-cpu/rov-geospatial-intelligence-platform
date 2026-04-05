import pandas as pd

def load_data(file):
    # 🔥 GARANTE que o arquivo seja lido do início
    file.seek(0)

    df = pd.read_csv(file, sep=None, engine='python')

    df.columns = df.columns.str.strip().str.lower()

    print("Colunas detectadas:", df.columns.tolist())

    if len(df.columns) == 0:
        raise ValueError("Arquivo vazio ou inválido")

    required_cols = ['latitude', 'longitude', 'depth']

    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df
