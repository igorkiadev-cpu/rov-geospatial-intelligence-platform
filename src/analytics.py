import pandas as pd

# 🔴 Anomaly detection
def detect_anomalies(df, threshold=2.5):
    df["depth_zscore"] = (df["depth"] - df["depth"].mean()) / df["depth"].std()
    df["anomaly"] = df["depth_zscore"].abs() > threshold
    return df

# 📊 Comparação de missões
def compare_missions(dfs):
    df_all = pd.concat(dfs)

    summary = df_all.groupby("mission").agg({
        "depth": ["max", "min", "mean"],
        "latitude": "count"
    }).reset_index()

    return df_all, summary
