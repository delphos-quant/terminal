import dash
import plotly.graph_objects as go
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate

from plotly import express

import pandas
from datetime import datetime, timedelta

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

def function_4(value): 
    return dash_table.DataTable(
        id='table',
        columns=[
            {"name": "Stock", "id": "Stock"},
            {"name": "PriceNow", "id": "PriceNow"},
            {"name": "AveragePriceYesterday", "id": "AveragePriceYesterday"},
            {"name": "AveragePriceBeforeYesterday", "id": "AveragePriceBeforeYesterday"},
        ],
        data = [
            {"Stock": "GOOG", "PriceNow": "1500", "AveragePriceYesterday": "1490", "AveragePriceBeforeYesterday": "1485"},
            {"Stock": "AAPL", "PriceNow": "200", "AveragePriceYesterday": "195", "AveragePriceBeforeYesterday": "190"},
            {"Stock": "AMZN", "PriceNow": "3100", "AveragePriceYesterday": "3080", "AveragePriceBeforeYesterday": "3060"},
            {"Stock": "MSFT", "PriceNow": "250", "AveragePriceYesterday": "245", "AveragePriceBeforeYesterday": "240"},
        ],
        style_cell_conditional=[
            {'if': {'column_id': 'Stock'},
             'textAlign': 'center'},
            {'if': {'column_id': 'PriceNow'},
             'textAlign': 'center'},
            {'if': {'column_id': 'AveragePriceYesterday'},
             'textAlign': 'center'},
            {'if': {'column_id': 'AveragePriceBeforeYesterday'},
             'textAlign': 'center'}
        ]
    )

def function_5(value): 
    children = []
    reshaped_data = {
        "GOOG": ["1500", "1490", "1485"],
        "AAPL": ["200", "195", "190"],
        "AMZN": ["3100", "3080", "3060"],
        "MSFT": ["250", "245", "240"],
    }

    # creating a DataFrame
    df = pandas.DataFrame(reshaped_data)

    # changing the index to dates
    df.index = [datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1), datetime.now()]
    df.index.name = 'Date'
    
    fig = express.line(df.astype(float), x=df.index, y=df.columns)

    fig.update_layout(
        title="Stock Price Comparison",
        xaxis_title="Time",
        yaxis_title="Price",
    )

    return dcc.Graph(figure=fig)

    # for row in data:
    #     fig_individual = go.Figure()
    #     fig_individual.add_trace(go.Scatter(x=['Before Yesterday', 'Yesterday', 'Now'], 
    #         y=[row['AveragePriceBeforeYesterday'], row['AveragePriceYesterday'], row['PriceNow']],
    #         mode='lines+markers',
    #         name=row['Stock']))
    #     fig_individual.update_layout(
    #         title=row['Stock'] + " Stock Price",
    #         xaxis_title="Time",
    #         yaxis_title="Price",
    #     )
    #     children.append(dcc.Graph(figure=fig_individual))
    #     fig.add_trace(go.Scatter(x=['Before Yesterday', 'Yesterday', 'Now'], 
    #         y=[row['AveragePriceBeforeYesterday'], row['AveragePriceYesterday'], row['PriceNow']],
    #         mode='lines+markers',
    #         name=row['Stock']))
    #     fig.update_layout(
    #         title="Stock Price Comparison",
    #         xaxis_title="Time",
    #         yaxis_title="Price",
    #     )
    #     children.append(html.H3('Comparison Chart'))
    #     children.append(dcc.Graph(figure=fig))
    # return children
    

function_map = {
    "function_1": function_1,
    "function_2": function_2,
    "function_3": function_3, 
    "function_4": function_4, 
    "function_5": function_5, 
}

buttons = [
    {"label": "Acoes Petrobras", "id": "function_1"},
    {"label": "Acoes Petrobras Iradas", "id": "function_2"},
    {"label": "Acoes", "id": "function_3"},
    {"label": "Acoes Tab", "id": "function_4"},
    {"label": "Acoes Graphic", "id": "function_5"},
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
