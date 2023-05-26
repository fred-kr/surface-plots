from typing import List, Tuple

import numpy as np
import plotly.graph_objects as go
from dash import dash_table, html

BACKGROUND_COLOR = "#999"
LINE_COLOR = "black"
LINE_WIDTH = 5
TICK_COLOR = "white"
TICK_FONT = dict(size=21, color="black", family="Arial")
TICK_LEN = 20
TICK_WIDTH = 5
ANNOTATION_FONT = dict(size=35, color="black", family="Arial")

COLOR_SCALES: dict[str, List[str]] = {
    'Set3': [
        "#8DD3C7",
        "#FFFFB3",
        "#BEBADA",
        "#FB8072",
        "#80B1D3",
        "#FDB462",
        "#B3DE69",
        "#FCCDE5",
        "#D9D9D9",
        "#BC80BD",
        "#CCEBC5",
        "#FFED6F",
    ],
    'R_rainbow_10': [
        "#FF0000",
        "#FF9900",
        "#CCFF00",
        "#33FF00",
        "#00FF66",
        "#00FFFF",
        "#0066FF",
        "#3300FF",
        "#CC00FF",
        "#FF0099",
    ],
    'D3': [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ],
    'Plotly': [
        "#636efa",
        "#EF553B",
        "#00cc96",
        "#ab63fa",
        "#FFA15A",
        "#19d3f3",
        "#FF6692",
        "#B6E880",
        "#FF97FF",
        "#FECB52",
    ],
    'G10': [
        "#3366CC",
        "#DC3912",
        "#FF9900",
        "#109618",
        "#990099",
        "#3B3EAC",
        "#0099C6",
        "#DD4477",
        "#66AA00",
        "#B82E2E",
    ],
    'Set1': [
        "#e41a1c",
        "#377eb8",
        "#4daf4a",
        "#984ea3",
        "#ff7f00",
        "#ffff33",
        "#a65628",
        "#f781bf",
        "#999999",
    ],
    'Light24': [
        '#FD3216', '#00FE35', '#6A76FC', '#FED4C4', '#FE00CE', '#0DF9FF', '#F6F926',
        '#FF9616', '#479B55', '#EEA6FB', '#DC587D', '#D626FF', '#6E899C', '#00B5F7',
        '#B68E00', '#C9FBE5', '#FF0092', '#22FFA7', '#E3EE9E', '#86CE00', '#BC7196',
        '#7E7DCD', '#FC6955', '#E48F72'
    ],
    'Vivid': [
        'rgb(229, 134, 6)', 'rgb(93, 105, 177)', 'rgb(82, 188, 163)', 'rgb(153, 201, 69)',
        'rgb(204, 97, 176)', 'rgb(36, 121, 108)', 'rgb(218, 165, 27)', 'rgb(47, 138, 196)',
        'rgb(118, 78, 159)', 'rgb(237, 100, 90)', 'rgb(165, 170, 153)'
    ],
    'Pastel': [
        'rgb(102, 197, 204)', 'rgb(246, 207, 113)', 'rgb(248, 156, 116)',
        'rgb(220, 176, 242)', 'rgb(135, 197, 95)', 'rgb(158, 185, 243)',
        'rgb(254, 136, 177)', 'rgb(201, 219, 116)', 'rgb(139, 224, 164)',
        'rgb(180, 151, 231)', 'rgb(179, 179, 179)'
    ]

}


def get_cam_data(
        cam_data: dict,
        input_graph: str
):
    """
    The get_cam_data function takes in the camera data and input graph name, and returns a table
    of the camera properties. The function first checks if the cam_data is None or does not
    contain `scene.camera`. If so, it returns a string explaining that you need to interact
    with the graph to see its properties. Otherwise, it creates an empty list called
    data and a dictionary called data_dict containing keys for each axis (x, y, z) as well as eye
    and center values. It then loops through each key in `[eye, center]` which are sub-keys of scene.

    Args:
        cam_data (dict): `relayoutData` property of a plotly figure
        input_graph (str): Name of input graph, just used for the id of the table

    Returns:
        An `html.Div` containing a `dash_table.DataTable` with the `eye` and `center` values
    """
    if cam_data is None or "scene.camera" not in cam_data:
        return "Interact with the graph to see camera properties"

    camera_data = cam_data["scene.camera"]
    data = []

    data_dict = {
        'Axis': ['x', 'y', 'z'],
        'Eye': [None, None, None],
        'Center': [None, None, None]}

    for key in ["eye", "center"]:
        if key in camera_data:
            sub_dict = camera_data[key]
            for i, sub_key in enumerate(
                    ['x', 'y', 'z']
            ):
                value = sub_dict.get(
                    sub_key,
                    None
                )
                data_dict[key.capitalize()][i] = value

    # Convert data dict to list of dicts
    data = [dict(
        zip(
            data_dict.keys(),
            values
        )
    ) for values in zip(
        *data_dict.values()
    )]

    return html.Div(
        [
            dash_table.DataTable(
                id=f"{input_graph}-cam-properties",
                columns=[
                    {
                        "name": "Axis",
                        "id": "Axis"},
                    {
                        "name": "Eye (Viewing Angle)",
                        "id": "Eye"},
                    {
                        "name": "Center",
                        "id": "Center"},
                ],
                data=data,
                style_cell={
                    "textAlign": "left"},
                style_header={
                    "backgroundColor": "rgb(230, 230, 230)",
                    "fontWeight": "bold"
                },
                style_table={
                    "width": "25%"},
            )
        ]
    )


def make_colorscale_distinct(n_colors: int, pal: str = "Set3") -> List[Tuple[float, str]]:
    """
    Generate a distinct colorscale for a given number of groups.

    Args:
        n_colors (int): Amount of groups to generate colors for.
        pal (str, optional): Name of color palette to take colors from. Defaults to "RCB_Set3_12".

    Raises:
        ValueError: Specified palette `pal` not found in COLOR_SCALES.

    Returns:
        List[Tuple[float, str]]: List of tuples of the form (scaled_value, color).
    """
    scaled_values = np.linspace(0, 1, n_colors + 1)

    if pal in COLOR_SCALES:
        colors = COLOR_SCALES[pal]
    else:
        raise ValueError(f"Palette {pal} not found in COLOR_SCALES")

    colors = colors[:n_colors]
    colorscale = []

    for i in range(n_colors):
        entry1 = (scaled_values[i], colors[i])
        entry2 = (scaled_values[i + 1], colors[i])
        colorscale.extend((entry1, entry2))

    return colorscale


def create_surface(
        x,
        y,
        z,
        colors_scaled,
        n_colors,
        opacity: float = 1.0,
        show_colorbar: bool = False,
        ambient_light: float = 0.9,
) -> go.Surface:
    """
    Takes values and produces a surface that can be added to a plotly plot.

    Args:
        x (ndarray): X-axis values.
        y (ndarray): Y-axis values.
        z (ndarray): Input data in form of a numpy ndarray (as returned by `get_inputs`).
        colors_scaled (List[Tuple[float, str]]): List of tuples of the form (scaled_value, color).
        n_colors (int): Amount of groups to generate colors for.
        opacity (float, optional): Opacity of the surface. Defaults to 1.
        show_colorbar (bool, optional): Whether to show colorbar. Defaults to False.
        ambient_light (float, optional): Ambient light of the surface. Defaults to 0.9.

    Returns:
        go.Surface: Surface to be added to a plotly plot

    """
    return go.Surface(
        x=x,
        y=y,
        z=z,
        opacity=opacity,
        colorscale=colors_scaled,
        cmin=0,
        cmax=n_colors,
        showscale=show_colorbar,
        colorbar=dict(
            tickmode="array",
            tickvals=np.arange(
                0, n_colors + 1, 2) if n_colors > 6 else np.arange(0, n_colors + 1, 1),
            ticktext=np.arange(
                0, n_colors + 1, 2) if n_colors > 6 else np.arange(0, n_colors + 1, 1),
            orientation="v",
            y=0.5,
            x=0.85,
            len=0.5,
            tickfont=dict(size=20),
        ),
        contours=dict(
            x=dict(show=True, start=0, end=10, size=2, color="black", width=5),
            y=dict(show=True, start=0, end=1.5,
                   size=0.5, color="black", width=5),
        ),
        hoverinfo="skip",
        lighting=dict(
            ambient=ambient_light,
            diffuse=0.5,
        ),
    )


def create_layout(
        x_label,
        y_label,
        z_label,
        surface_1_name,
        surface_2_name,
        surface_1_2d_list,
        surface_2_2d_list,
        x_scale=1.0,
        y_scale=0.5,
        z_scale=0.5
):

    # Check if surface_1_name contains "WPI" or "SEE"
    is_wpi = "WPI" in surface_1_name

    y_tick_labels_cs = ["0", "0.5", "1.0", "1.5"]
    y_tick_vals_cs = [0, 0.5, 1, 1.5]
    y_tick_labels_wpi = ["15", "12", "9", "6"]
    y_tick_vals_wpi = [15, 12, 9, 6]
    z_tick_labels_see = ["", "2", "4", "6", "8", "10", "12", "14"]
    z_tick_vals_see = [0, 2, 4, 6, 8, 10, 12, 14]
    z_tick_labels_wpi = ["", "2", "4", "6",
                         "8", "10", "12", "14", "16", "18", "20"]
    z_tick_vals_wpi = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    # Determine which tick labels and values to use based on surface_1_name
    z_tick_labels_shown = z_tick_labels_wpi if is_wpi else z_tick_labels_see
    z_tick_vals_shown = z_tick_vals_wpi if is_wpi else z_tick_vals_see

    annotation_1_z = _extracted_from_create_layout_31(surface_1_2d_list)
    annotation_2_z = _extracted_from_create_layout_31(surface_2_2d_list)
    return go.Layout(
        autosize=False,
        height=900,
        margin=dict(r=0, b=0, l=0, t=0, pad=0, autoexpand=True),
        title='',
        scene=dict(
            aspectmode="manual",
            aspectratio=dict(x=x_scale, y=y_scale, z=z_scale),
            xaxis=dict(
                backgroundcolor=BACKGROUND_COLOR,
                linecolor=LINE_COLOR,
                linewidth=LINE_WIDTH,
                mirror=True,
                range=[0, 10],
                showbackground=True,
                showgrid=True,
                showline=True,
                showticklabels=True,
                tickcolor=TICK_COLOR,
                tickfont=TICK_FONT,
                ticklen=TICK_LEN,
                tickmode="array",
                ticks="outside",
                ticktext=["0", "2", "4", "6", "8", "10"],
                tickvals=[0, 2, 4, 6, 8, 10],
                tickwidth=TICK_WIDTH,
                title='',
            ),
            yaxis=dict(
                backgroundcolor=BACKGROUND_COLOR,
                linecolor=LINE_COLOR,
                linewidth=LINE_WIDTH,
                mirror=True,
                range=[15, 6] if "WPI" in surface_1_name else [0.00, 1.5],
                showbackground=True,
                showgrid=True,
                showline=True,
                showticklabels=True,
                tickcolor=TICK_COLOR,
                tickfont=TICK_FONT,
                ticklen=TICK_LEN,
                tickmode="array",
                ticks="outside",
                ticktext=y_tick_labels_wpi if "WPI" in surface_1_name else y_tick_labels_cs,
                tickvals=y_tick_vals_wpi if "WPI" in surface_1_name else y_tick_vals_cs,
                tickwidth=TICK_WIDTH,
                title=''
            ),
            zaxis=dict(
                backgroundcolor=BACKGROUND_COLOR,
                linecolor=LINE_COLOR,
                linewidth=LINE_WIDTH,
                mirror=True,
                range=[0, 14] if "SEE" in surface_1_name else [0, 6],
                showbackground=True,
                showgrid=True,
                showline=True,
                showticklabels=True,
                tickcolor=TICK_COLOR,
                tickfont=TICK_FONT,
                ticklen=TICK_LEN,
                tickmode="array",
                ticks="outside",
                ticktext=z_tick_labels_shown,
                tickvals=z_tick_vals_shown,
                tickwidth=TICK_WIDTH,
                title=''
            ),
            annotations=[
                dict(
                    x=3,
                    y=0.2,
                    z=0,
                    textangle=21,
                    yshift=-71,
                    xshift=20,
                    text=x_label,
                    showarrow=False,
                    font=ANNOTATION_FONT,
                    xanchor="center",
                    yanchor="top",
                ),
                dict(
                    x=9.8,
                    y=0.25,
                    z=0,
                    textangle=-43,
                    text=y_label,
                    showarrow=False,
                    font=ANNOTATION_FONT,
                    xanchor="left",
                    xshift=78,
                    yanchor="middle",
                ),
                dict(
                    x=0,
                    y=0.02,
                    z=3 if "SEE" not in surface_1_name else 7,
                    textangle=-94,
                    text=z_label,
                    showarrow=False,
                    font=ANNOTATION_FONT,
                    xanchor="right",
                    xshift=-70,
                    yanchor="middle",
                ),
                dict(
                    x=10,
                    y=1.5 if "WPI" not in surface_1_name else 0.5,
                    z=annotation_1_z,
                    bgcolor="white",
                    bordercolor="black",
                    text=surface_1_name,
                    font=dict(size=21),
                    arrowhead=6,
                    ax=70,
                    ay=-20,
                    xanchor="left",
                ),
                dict(
                    x=10,
                    y=1.5 if "WPI" not in surface_1_name else 0.5,
                    z=annotation_2_z,
                    bgcolor="white",
                    bordercolor="black",
                    text=surface_2_name,
                    font=dict(size=21),
                    arrowhead=6,
                    ax=70,
                    ay=20,
                    xanchor="left",
                )
            ],
            camera=dict(
                center=dict(x=0.2, y=0.1, z=0),
                eye=dict(x=0.96, y=-1.12, z=0.26),
            ),
        ),
    )


# TODO Rename this here and in `create_layout`
def _extracted_from_create_layout_31(arg0):
    len(arg0[0]) if arg0 else 0
    len(arg0)
    return arg0[-1][-1]


def percentage_difference(base_array: np.ndarray, compare_array: np.ndarray) -> np.ndarray:
    # Calculate the absolute difference between the arrays
    difference = np.abs(base_array - compare_array)

    # Determine the maximum and minimum values in the base array
    max_value = np.max(base_array)
    min_value = np.min(base_array)

    # Normalize the differences by the maximum possible difference in the base array
    max_possible_difference = max_value - min_value
    normalized_difference = difference / max_possible_difference

    return normalized_difference * 100


def add_traces_to_figure(figure, data):
    """
    Adds multiple scatter3d and cone traces to a plotly figure.

    Args:
        figure (plotly.graph_objs._figure.Figure): The figure to which the traces are added.
        data (list[dict]): A list of data dictionaries where each dictionary represents a trace.
            Each dictionary must contain the following keys:
            - 'type': 'scatter3d' or 'cone'
            - 'x', 'y', 'z': Coordinates.
            - 'text': (optional) Text to be displayed. This is only required for scatter3d traces.
            - 'color': (optional) RGB color for the trace. This is only required for cone traces.
    """
    for trace in data:
        if trace['type'] == 'scatter3d':
            figure.add_scatter3d(
                x=trace['x'],
                y=trace['y'],
                z=trace['z'],
                mode='text',
                text=trace['text'],
                textposition="top center",
                textfont=dict(
                    family="Arial",
                    size=18,
                    color="black",
                ),
                showlegend=False,
            )
        elif trace['type'] == 'cone':
            figure.add_cone(
                x=trace['x'],
                y=trace['y'],
                z=trace['z'],
                u=[0],
                v=[0],
                w=[-2],
                anchor="tip",
                colorscale=[[0, trace['color']], [1, trace['color']]],
                showscale=False,
                showlegend=False,
            )
    return figure
