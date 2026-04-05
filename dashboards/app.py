import streamlit as st
import pandas as pd
import io

st.title("🌊 ROV Mission Intelligence Platform")

uploaded_file = st.file_uploader("Upload ROV CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # 🔥 leitura FORÇADA correta
        content = uploaded_file.getvalue().decode("utf-8")

        # DEBUG
        st.write("Preview bruto do arquivo:")
        st.text(content[:200])

        # lê dataframe
        df = pd.read_csv(io.StringIO(content), sep=None, engine='python')

        # DEBUG COLUNAS
        st.write("Colunas detectadas:", df.columns.tolist())

        # normalização
        df.columns = df.columns.str.strip().str.lower()

        required_columns = ['latitude', 'longitude', 'depth']

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            st.error(f"Missing required columns: {missing}")
        else:
            st.success("CSV carregado com sucesso!")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error processing file: {e}")
