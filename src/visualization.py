import plotly.express as px

def map_2d(df):
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="depth",
        zoom=5,
        height=600
    )
    fig.update_layout(mapbox_style="open-street-map")
    return fig


def map_3d(df):
    df["depth_visual"] = -df["depth"]

    fig = px.scatter_3d(
        df,
        x="longitude",
        y="latitude",
        z="depth_visual",
        color="depth",
        height=700
    )
    return fig


def anomalies_map(df):
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="anomaly",
        color_discrete_map={True: "red", False: "blue"},
        zoom=5,
        height=600
    )
    fig.update_layout(mapbox_style="open-street-map")
    return fig


def bathymetry_map(df):
    fig = px.density_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        z="depth",
        radius=10,
        zoom=5,
        height=600
    )
    fig.update_layout(mapbox_style="open-street-map")
    return fig
