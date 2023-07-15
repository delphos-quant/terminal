import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

def function_1(_):
    return html.Div([
        html.H3("Sopa de Macaco"),
        html.Button("Volatilidade mensal"),
        html.Button("Volatilidade Anual", id={'type': 'dynamic-button', 'index': 'vol-mensal'}, n_clicks=0),
        html.Div(id={'type': 'dynamic-output', 'index': 'vol-mensal'})
    ])

def function_2(value):
    return value ** 3

def function_3(value): 
    return value ** (value ** value)

function_map = {
    "function_1": function_1,
    "function_2": function_2,
    "function_3": function_3, 
}

buttons = [
    {"label": "Acoes Petrobras", "id": "function_1"},
    {"label": "Acoes Petrobras Iradas", "id": "function_2"},
    {"label": "Acoes", "id": "function_3"},
]


app.layout = html.Div(
    [
        html.H1("Search App"),
        dcc.Input(
            id="search-bar",
            placeholder="Enter search term",
            style={"width": "300px"},
        ),
        html.H3("Search Results"),
        html.Div(id="search-results"),
        html.P(id="sub-menu"),
    ]
)


@app.callback(
    Output("search-results", "children"),
    [Input("search-bar", "value")]
)
def update_search_results(search_term):
    if not search_term:
        return html.P(f"Search Term: {search_term}")

    
    filtered_options = [option for option in buttons if all(word.lower() in option["label"].lower() for word in search_term.split())]



    return html.Div(
        [
            html.P(f"Search Term: {search_term}"),
            html.Div([html.Button(button['label'], id={'type': 'dynamic-button', 'index': button['id']}, n_clicks=0) for button in filtered_options]),
            html.Div([html.Div(id={'type': 'dynamic-output', 'index': button['id']}) for button in filtered_options])
        ]
    )


@app.callback(
    Output({'type': 'dynamic-output', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-button', 'index': MATCH}, 'n_clicks'),
)
def update_output(n_clicks):
    if n_clicks is None or n_clicks <= 0:
        raise PreventUpdate
    else:
        id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        button_id = eval(id)['index']
        function_to_execute = function_map[button_id]
        return function_to_execute(n_clicks)


if __name__ == "__main__":
    app.run_server(debug=True)
