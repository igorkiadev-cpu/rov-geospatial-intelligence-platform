import pandas as pd
import io

def load_data(file):
    try:
        if file is None:
            raise ValueError("No file uploaded")

        # converte upload para texto corretamente
        string_data = file.getvalue().decode("utf-8")

        # lê como CSV real
        df = pd.read_csv(io.StringIO(string_data), sep=None, engine='python')

        print("COLUNAS LIDAS:", df.columns.tolist())

        df.columns = df.columns.str.strip().str.lower()

        required_columns = ['latitude', 'longitude', 'depth']

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        return df

    except Exception as e:
        raise ValueError(f"Error processing file: {e}")
