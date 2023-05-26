import pickle

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Input, Output, State, callback_context, dash, dcc, exceptions, html
from plotly_helpers import (  # noqa: E402
    add_traces_to_figure,
    create_layout,
    create_surface,
    get_cam_data,
)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc_css]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                prevent_initial_callbacks='initial_duplicate')  # type: ignore

server = app.server

with open('E:/projects/surface-plots/data/bin/data_v4.pickle', 'rb') as file:
    surface_data = pickle.load(file)


traces = []

for key in surface_data.keys():
    group = surface_data[key]
    combinations = group['combinations']
    for names in combinations:
        data_1 = group['files'][names[0]].to_numpy()
        data_2 = group['files'][names[1]].to_numpy()

        if "WIP" in names[0]:
            data_1 = data_1.T
            data_2 = data_2.T

        data_1_max = data_1.max()
        data_2_max = data_2.max()

        surface_1 = create_surface(
            x=group["axes"]["x"]["values"],
            y=group["axes"]["y"]["values"],
            z=data_1.tolist(),
            colors_scaled=group["colorscale"][names[0]],
            n_colors=group["n_colors"][names[0]
                                       ] if "SEE" not in names[0] else group["n_colors"][names[0]] * 2,
            opacity=1.0 if data_2_max > data_1_max else 0.8,
            show_colorbar=False if data_2_max > data_1_max else True,
            ambient_light=0.9 if data_2_max > data_1_max else 0.5,
        )
        surface_2 = create_surface(
            x=group["axes"]["x"]["values"],
            y=group["axes"]["y"]["values"],
            z=data_2.tolist(),
            colors_scaled=group["colorscale"][names[1]],
            n_colors=group["n_colors"][names[1]
                                       ] if "SEE" not in names[1] else group["n_colors"][names[1]] * 2,
            opacity=0.8 if data_2_max > data_1_max else 1.0,
            show_colorbar=True if data_2_max > data_1_max else False,
            ambient_light=0.5 if data_2_max > data_1_max else 0.9,
        )
        traces.append([surface_1, surface_2])


dropdown_options = []
layouts = []

for key in surface_data.keys():
    group = surface_data[key]
    for i in range(len(group['combinations'])):
        surf_name_1 = group['combinations'][i][0]
        surf_name_2 = group['combinations'][i][1]
        dropdown_options.append(
            {"label": f"{surf_name_1}+{surf_name_2}", "value": f"{surf_name_1}+{surf_name_2}"})

        s1 = group["files"][surf_name_1].to_numpy()
        s2 = group["files"][surf_name_2].to_numpy()

        layout = create_layout(
            x_label="Wave Height [m]",
            y_label="Wave Period [s]" if "WPI" in surf_name_1 else "Current Speed [m/s]",
            z_label="SEE Index" if "SEE" in surf_name_1 else "EVRD Index",
            surface_1_name=surf_name_1,
            surface_2_name=surf_name_2,
            surface_1_2d_list=s1.tolist(),
            surface_2_2d_list=s2.tolist(),
            x_scale=1.0,
            y_scale=0.5,
            z_scale=0.5,
        )
        layouts.append(layout)


figures = {
    option["value"]: go.Figure(data=traces[i], layout=layouts[i]).to_dict()
    for i, option in enumerate(dropdown_options)
}


app.layout = dbc.Container(
    [
        dcc.Store(id="figure-store", data=figures),
        html.H1(
            "SEE Index Visualisations",
            className="text-primary text-center mb-3"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id="cam-output"
                        ),
                    ],
                    width=1
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="plot-window",
                            config={
                                "editable": True,
                                "edits": {
                                    "colorbarTitleText": False,
                                    "annotationText": False,
                                    "annotationPosition": True,
                                    "annotationTail": True,
                                    "titleText": True,
                                },
                                "showEditInChartStudio": True,
                                "plotlyServerURL": "https://chart-studio.plotly.com",
                                "toImageButtonOptions": {
                                    "format": "png",  # one of png, svg, jpeg, webp
                                }
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Select a plot to view:"
                                ),
                                dcc.Dropdown(
                                    id="graph-selector",
                                    options=dropdown_options,
                                    value=list(surface_data.items())[
                                        1][1]["combinations"][0][0] + "+" + list(surface_data.items())[1][1]["combinations"][0][1],
                                    clearable=False,
                                    style={
                                        "width": "50%"}
                                ),
                            ]
                        ),
                    ],
                    width=8
                ),
                dbc.Col([
                    html.Span([
                        html.Label('X:'),
                        dcc.Input(id='input-x', value=2, type='number'),
                        html.Label('Y:'),
                        dcc.Input(id='input-y', value=0.5, type='number'),
                        html.Label('Z:'),
                        dcc.Input(id='input-z', value=2.15, type='number'),
                        html.Label('Text:'),
                        dcc.Input(id='input-text',
                                  value='Max working conditions', type='text'),
                        html.Label('Color:'),
                        dcc.Input(id='input-color',
                                  value='rgb(0, 255, 0)', type='text'),
                        html.Button('Add Trace', id='add-trace-button'),
                    ], style={
                        "width": "50%",
                        "display": "inline-block"
                    }),
                ], width=2),


            ],
        ),
        # html.Hr(),
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             [
        #                 dcc.Graph(
        #                     id="diff-window",
        #                     figure=diffs,
        #                     config={
        #                         "editable": True,
        #                         "edits": {
        #                             "colorbarTitleText": False,
        #                             "annotationText": False,
        #                             "annotationPosition": True,
        #                             "annotationTail": True,
        #                             "titleText": True,
        #                         },
        #                         "showEditInChartStudio": True,
        #                         "plotlyServerURL": "https://chart-studio.plotly.com",
        #                         "toImageButtonOptions": {
        #                             "format": "png",  # one of png, svg, jpeg, webp
        #                         }
        #                     },
        #                 ),
        #             ],
        #             width=8
        #         )
        #     ],
        #     justify="center"
        # )

    ],
    fluid=True
)


@app.callback(
    Output(
        "cam-output",
        "children"
    ),
    Input(
        "plot-window",
        "relayoutData"
    )
)
def update_camera_output(
        relayout_data
):
    return get_cam_data(
        relayout_data,
        "main"
    )


@app.callback(
    [
        Output(
            'plot-window',
            'figure',
            allow_duplicate=True
        ),
        Output(
            'figure-store',
            'data',
            allow_duplicate=True
        )
    ],
    Input(
        "graph-selector",
        "value",
    ),
    State(
        "figure-store",
        "data"
    ),

)
def select_graph(title, figures_dict):

    surf_name_1 = title.split("+")[0]
    surf_name_2 = title.split("+")[1]

    if "WPI" in title and "SEE" in title:
        group = 3
    elif "WPI" in title and "EV" in title:
        group = 2
    elif "WPI" not in title and "SEE" in title:
        group = 1
    elif "WPI" not in title and "EV" in title:
        group = 0
    else:
        raise ValueError("Invalid title")

    data_1_2d_list = list(surface_data.items())[
        group][1]['files'][surf_name_1].to_numpy()
    data_2_2d_list = list(surface_data.items())[
        group][1]['files'][surf_name_2].to_numpy()

    layout = create_layout(
        x_label="Wave Height [m]",
        y_label="Wave Period [s]" if "WPI" in surf_name_1 else "Current Speed [m/s]",
        z_label="SEE Index" if "SEE" in surf_name_1 else "EVRD Index",
        surface_1_name=surf_name_1,
        surface_2_name=surf_name_2,
        surface_1_2d_list=data_1_2d_list.tolist(),
        surface_2_2d_list=data_2_2d_list.tolist(),
        x_scale=1.0,
        y_scale=0.5,
        z_scale=0.5
    )

    fig = go.Figure(figures_dict[title])
    fig.update_layout(layout, uirevision=title)

    # Update the figure in the figures_dict
    figures_dict[title] = fig.to_dict()

    # Store the updated figures_dict in the figure-store
    return fig, figures_dict


# Callback for adding cones + text to figure as site markers
@app.callback(
    # Update the data in the figure-store component
    Output('figure-store', 'data', allow_duplicate=True),
    Input('add-trace-button', 'n_clicks'),
    State('input-x', 'value'),
    State('input-y', 'value'),
    State('input-z', 'value'),
    State('input-text', 'value'),
    State('input-color', 'value'),
    State('plot-window', 'figure'),
    State('graph-selector', 'value'),
    State('figure-store', 'data')
)
def add_trace(n_clicks, x, y, z, text, color, figure_dict, selected_graph, figures_dict):
    if n_clicks is None:
        # Button has not been clicked yet
        return figures_dict

    # Convert the figure dictionary back to a Figure object
    figure = go.Figure(figure_dict)

    # Define your add_traces_to_figure function here
    data_dicts = [
        {'type': 'scatter3d', 'x': [x], 'y': [y], 'z': [z], 'text': [text]},
        {'type': 'cone', 'x': [x], 'y': [y], 'z': [z-1], 'color': color}
    ]
    add_traces_to_figure(figure, data_dicts)

    # Update the figures dictionary with the new figure
    figures_dict[selected_graph] = figure.to_dict()

    # Return the updated figures dictionary
    return figures_dict


@app.callback(
    # Update the figure displayed in the Graph component
    Output(
        'plot-window',
        'figure',
        allow_duplicate=True
    ),

    # Take the data from the figure-store component
    [
        Input('figure-store', 'data'),
        Input('graph-selector', 'value'),
    ]
)
def update_graph(figures_dict, selected_graph):
    ctx = callback_context
    if ctx.triggered[0]['prop_id'] == 'figure-store.data':
        return go.Figure(figures_dict[selected_graph])

    # In case the callback was triggered by the 'graph-selector' value change, do nothing.
    # The 'select_graph' callback will take care of this change.
    else:
        raise exceptions.PreventUpdate


if __name__ == '__main__':
    app.run(debug=True)
