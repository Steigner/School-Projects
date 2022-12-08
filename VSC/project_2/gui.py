#                   ---GUI script---

# libraries for create html/dash gui
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# werkzung for eliminated disturbing routing in standard output 
import logging

import numpy as np

from ann import ANN
import time

ann = ANN()
ann.show_rastrigin()
fig = ann.graph.fig

# import basic open-source layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# ass python flask server, this is basic set up + setting for all monitors
app = dash.Dash(
    __name__,
    external_stylesheets = external_stylesheets,
    meta_tags = [
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# This huge part represents gui in form web-based app
# in this app is set basic introduction in form md. I don't if is
# neccesary any deeply comment, this just represent html/plotly/dash combination to
# create humble GUI.
app.layout = html.Div([
    html.Div([
        dcc.Markdown(
            '''
            ### Adaptive ANN modeling
            **Fast introduction**
            
            This humble GUI represent simple binary ANN classificator. This
            classificator is programmed in **python3** with using libraries:
            
            * Tensorflow -> Keras
            * Numpy -> There is possibillity use Cupy for faster generating points
            * Plotly -> Dash

            **Rastrigin Function** 
            
            ```python
                            f(x) = 10*d + SUM[i=0;i=d]([xi**2 - 10cos(2*PI*xi)])
            ```
            
            **Schwefel Function** 
            
            ```python
                            f(x) = 418.9829*d - SUM[i=0;i=d]([xi * sin(sqrt(abs(xi)))])
            ```

            ** About program **
            
            Programme is control from simple GUI buttons, first you choose function which, you want to
            approximate(defaul Rastrigin), and then hit button start. Process can be watched in console/terminal.
            * Architecture of rastrigin function: relu(200, 125, 64, 9, 6); linear(1);
            * Architecture of schwefell function: relu(500, 150, 64, 18); linear(1);
            * Optimizer: Nadam - combines NAG and Adam optimizers.
            * Prametres: 5 iterations, 500 epochs, 10 000 points

            Author - Martin Juricek
            [github](https://github.com/Steigner)

            ** About course **

            VSC - Neural Networks and Evolution Methods

            Supervisor - doc. Ing. Radomil Matoušek, Ph.D.

            Teacher - Ing. Ing. Ladislav Dobrovsky

            Department - [Institute of Automation and Computer Science](https://uai.fme.vutbr.cz/en/)

            [Faculty of Mechanical Engineering BUT](https://www.fme.vutbr.cz/en)

            '''
        ),
        html.Button('Rastrigin Function', id = 'rastrigin'),
        html.Button('Schwefel Function', id = 'schwefel'),
        html.Button('start', id = 'start'),
        html.Div(id='info',style={'margin-top': '5%'}),
    ],
        style={
            'margin-left': '2%',
            'width': '35%',
            'float':'left'
        }
    ),
    
    html.Div([
        dcc.Loading(
            id = "loading-icon",
            type = "circle",
            fullscreen = True,
            children = [html.Div(
                dcc.Graph(
                    id='graph',
                    figure=fig,
                    style={'height': '90vh'}
                )
            )]
        ),
    ],
        style = {
            'width': '60%',
            'height': '100%',
            'float': 'right'
        }
    )
])

@app.callback(
    Output('graph', 'figure'),
    Output('info','children'),
    
    Input('rastrigin','n_clicks'),
    Input('schwefel','n_clicks'),
    Input('start','n_clicks'),
)
def update_output(btn0, btn1, btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'rastrigin' in changed_id:
        ann.switch = 0
        ann.show_rastrigin()
        return ann.graph.fig, "- RASTRIGIN FUNCTION -"

    elif 'schwefel' in changed_id:
        ann.switch = 1
        ann.show_schwefel()
        return ann.graph.fig, "- SCHWEFEL FUNCTION -"
    
    elif 'start' in changed_id:
        ann.net()
        return ann.graph.fig, "- DONE -"

    else:
        return fig, "- INFO -"

if __name__ == '__main__':
    # only error outputs
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    # run local server
    app.run_server(
        host = '127.0.0.1', 
        port = '14508',
        debug = False,
    )
