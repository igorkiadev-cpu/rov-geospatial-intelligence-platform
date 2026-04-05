import plotly.express as px
import plotly.graph_objects as go

# -----------------------
# 2D MAP (COM TRAJETÓRIA)
# -----------------------
def map_2d(df):
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="depth",
        zoom=5,
        height=500
    )

    # linha da trajetória
    fig.add_trace(go.Scattermapbox(
        lat=df["latitude"],
        lon=df["longitude"],
        mode="lines",
        line=dict(width=2),
        name="Trajectory"
    ))

    fig.update_layout(mapbox_style="open-street-map")
    return fig


# -----------------------
# 3D MAP
# -----------------------
def map_3d(df):
    fig = px.scatter_3d(
        df,
        x="longitude",
        y="latitude",
        z="depth",
        color="depth"
    )

    fig.update_traces(marker=dict(size=4))
    return fig


# -----------------------
# ANOMALIES MAP
# -----------------------
def anomalies_map(df):
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="anomaly",
        zoom=5,
        height=500
    )

    fig.update_layout(mapbox_style="open-street-map")
    return fig


# -----------------------
# BATHYMETRY
# -----------------------
def bathymetry_map(df):
    fig = px.density_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        z="depth",
        radius=20,
        zoom=5,
        height=500
    )

    fig.update_layout(mapbox_style="open-street-map")
    return fig
