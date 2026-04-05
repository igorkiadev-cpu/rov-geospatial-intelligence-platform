import pandas as pd

def load_data(file):
    try:
        # lê com detecção automática de separador
        df = pd.read_csv(file, sep=None, engine='python', encoding='utf-8-sig')

        # DEBUG (pode remover depois)
        print("COLUNAS LIDAS:", df.columns.tolist())

        # limpa nomes das colunas
        df.columns = df.columns.str.strip().str.lower()

        # colunas obrigatórias
        required_columns = ['latitude', 'longitude', 'depth']

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        return df

    except Exception as e:
        raise ValueError(f"Error processing file: {e}")
