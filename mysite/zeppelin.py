from dash import dash, html, dcc

# custom files
import backend

app = dash.Dash()

crypto_graph = backend.make_graph()
updated = backend.get_updated()

app.layout = html.Div(children=[

    html.H2(children=f"Last updated: {updated} UTC"),
    #html.Div(children="Menu"),
    dcc.Dropdown(['Current Coin Prices', 'Our Trades', 'Our Returns'], 'Current Coin Prices'),
    dcc.Graph(id='crypto graph', figure=crypto_graph),
    dcc.Interval()
    #, generate_table(data)
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

