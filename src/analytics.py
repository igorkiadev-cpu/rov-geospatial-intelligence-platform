import numpy as np

def detect_anomalies(df):
    df = df.copy()

    # variação de profundidade
    df["depth_diff"] = df["depth"].diff().abs()

    # velocidade horizontal (aproximada)
    df["lat_diff"] = df["latitude"].diff().abs()
    df["lon_diff"] = df["longitude"].diff().abs()
    df["movement"] = np.sqrt(df["lat_diff"]**2 + df["lon_diff"]**2)

    # thresholds (ajustáveis)
    depth_threshold = df["depth_diff"].mean() + 2 * df["depth_diff"].std()
    movement_threshold = df["movement"].mean() + 2 * df["movement"].std()

    # regras de anomalia
    df["anomaly"] = (
        (df["depth_diff"] > depth_threshold) |
        (df["movement"] > movement_threshold)
    )

    return df
