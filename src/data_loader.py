import pandas as pd

def load_data(file):
    # ❗ Garante que o arquivo existe
    if file is None:
        raise ValueError("No file uploaded")

    # 🔥 Volta pro início (resolve erro de arquivo vazio)
    file.seek(0)

    try:
        # 🔥 Auto-detecta separador
        df = pd.read_csv(file, sep=None, engine='python')
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

    # ❗ Se não leu nada
    if df.empty:
        raise ValueError("Arquivo vazio ou sem dados")

    # 🔥 Padroniza colunas
    df.columns = df.columns.str.strip().str.lower()

    print("Colunas detectadas:", df.columns.tolist())

    # 🔥 Se veio tudo em uma coluna (CSV quebrado)
    if len(df.columns) == 1:
        file.seek(0)
        df = pd.read_csv(file, sep=',')
        df.columns = df.columns.str.strip().str.lower()

    # 🔥 Colunas obrigatórias
    required_cols = ['latitude', 'longitude', 'depth']

    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # 🔥 Converte tipos (evita bug silencioso)
    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 🔥 Remove linhas inválidas
    df = df.dropna(subset=required_cols)

    return df
