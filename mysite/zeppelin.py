#!/usr/bin/env python
'''
Authored by Isaiah Terrell-Perica
05/26/2023

- This file handles the display of the Zeppelin web-app.  
- A Google Analytics tag is included but is not currently needed.
- The web-app requires 
    1) a dropdown selector with options
    2) indicators of interest clearly visualized
    3) a summary of the connected accounts' information
- Zeppelin uses Binance for price data and account info
'''

from dash import dash, html, dcc, Input, Output

# Custom files
import backend
from websocket_streams import start_websocket

app = dash.Dash(__name__)

# Google Analytics tag
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-WMWKTVG0WM"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-WMWKTVG0WM');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Start websocket and
start_websocket()
backend.register_callbacks(app)
# Retrieving components for dashboard display
crypto_graph = backend.make_graph()
updated = backend.last_updated()
time_interval=1000

# dashboard layout
app.layout = html.Div(children=[
    html.H2(children=f"Last update: {updated} UTC"),
    #html.Div(children="Menu"),
    dcc.Dropdown(['Coin Prices (Real Time)', 'Our Trades', 'Our Returns'], 'Current Coin Prices', id='dropdown'),
    dcc.Graph(id='crypto-graph', figure=crypto_graph),
    dcc.Interval(id='interval', interval=time_interval)
    #, generate_table(data)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)