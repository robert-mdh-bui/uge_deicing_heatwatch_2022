import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Iframe(
            id="my-output",
            src="assets/ORD.html",
            style={'height': '495px',
                   'width': '100%'}
        ),
        dcc.Input(
            id='textinput',
            placeholder='Enter 3-letter IATA code',
            type='text',
            value='ORD'
        )
    ]
)


@app.callback(
    Output('my-output', 'src'),
    Input('textinput', 'value'),
    prevent_initial_call=True
)
def update_output_div(input_value):
    return f'assets/{input_value}.html'


if __name__ == '__main__':
    app.run_server()
