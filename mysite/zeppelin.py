import dash
import dash_core_components as dcc
import dash_html_components as html

# user-made files
import research


app = dash.Dash()

crypto_graph = research.make_graph()

app.layout = html.Div(children=[
    html.H1(children="Graph"),
    html.Div(children="Test web app"),

    dcc.Graph(
        id='crypto graph',
        figure=crypto_graph
    )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

