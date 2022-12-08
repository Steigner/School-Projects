#                   ---GUI script---

# libraries for create html/dash gui
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# werkzung for eliminated disturbing routing in standard output 
import logging

# csv for import csv file 
import csv

# import Integral script with class ANN
from net import ANN

# import basic open-source layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# ass python flask server, this is basic set up + setting for all monitors
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# call instance of ANN an set fig
ann = ANN()
ann.net_gp()
fig = ann.graph.fig

# This huge part represents gui in form web-based app
# in this app is set basic introduction in form md. I don't if is
# neccesary any deeply comment, this just represent html/plotly/dash combination to
# create humble GUI.
app.layout = html.Div([
    html.Div([
        dcc.Markdown(
            '''
            ## simple ANN classificator
            **Fast introduction**
            
            This humble GUI represent simple binary ANN classificator. This
            classificator is programmed in **python3** with using libraries:
            
            * Tensorflow -> Keras
            * Numpy -> There is possibillity use Cupy for faster generating points
            * Plotly -> Dash

            **Classification equation form:** 
            
            ```python
                            0.4444444 * (x1 + 2)**2 + 2.3668639 * (x2 - 3)**2 < 1
            ```

            ** About program **

            Main program contain 1 homing dropdown menu, and 5 basic buttons. First is for refresh data(prevent from gets stuck), second is reset(blank graph), 
            third init(init graph with generated points), penultimate show equation shape, and last one show approximate bounderies by defined classificator.
            In dropdown menu you can loaded data from csv file, but this is only simple csv load file, for web deploy is necessary
            to programme parser and last but not least is there option to train again defined ann. Inputs can be also added
            by basic gui input, which you find in dropdown menu. In my opinion less inputs is better. In lower part is defined simple INFO label.
            One of the possible disadvantages is, that GUI will be not responsive for all type of monitors, so if you have screen of laptop as calculator, some
            buttons and inputs will be disturbing. This will be maybe in future debuged. The basckground theme is default Dash open-source, but can be change for example [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/).
            
            Author - Martin Juricek
            [github](https://github.com/Steigner/VSC)

            ** About course **

            VSC - Neural Networks and Evolution Methods

            Supervisor - doc. Ing. Radomil Matoušek, Ph.D.

            Teacher - Ing. Ing. Ladislav Dobrovsky

            Department - [Institute of Automation and Computer Science](https://uai.fme.vutbr.cz/en/)

            [Faculty of Mechanical Engineering BUT](https://www.fme.vutbr.cz/en)

            '''
        ),
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
            type="circle",
            fullscreen=True,
            children=[html.Div(
                dcc.Graph(
                    id='graph',
                    figure=fig
                )
            )]
        ),
        html.A(html.Button('Refresh Data',style={'margin-left':'22%'}),href='/'),
        html.Button('Reset', id='reset'),
        html.Button('Init', id='init'),
        html.Button('Elipse', id='elipse'),
        html.Button('Aprox', id='aprox',style={'margin-bottom':'5%'}),

        html.Div(
            style={
                'width': '27%',
                'margin-left': '35%',
            }, 
            children=[
                dcc.Dropdown(
                    id='drop-menu',
                    placeholder='Select main features ...',
                    options=[
                        {'label': 'Train ANN', 'value': 'o_1'},
                        {'label': 'Upload csv file', 'value': 'o_2'},
                        {'label': 'Inputs', 'value': 'o_3'},
                    ],
            ),
        ]),

        html.Button('Train', id='b_train'),

        dcc.Input(id='x1', type='text', placeholder="x1"),
        dcc.Input(id='x2', type='text', placeholder="x2"),
            
        html.Button('Test', id='b_test'),
        
        dcc.Upload(
            id='upload-data',
            children=html.Div(id='drag'),
            style={
                'visibility':'hidden' 
            },
            multiple=False
        ),
        html.Div(id='output-data-upload'),

        html.Div(id='info',style={'margin-top': '5%','text-align': 'center'}),

    ],
        style={
            'width': '60%',
            'float':'right',
            'margin-right': '2%',
        }
    )
])

# This callback, takes care of visibility any buttons etc... 
@app.callback(
    Output('b_train','style'),
    Output('x1','style'),
    Output('x2','style'),
    Output('b_test','style'),
    Output('upload-data', 'style'),
    Output('drag', 'children'),
    Input('drop-menu', 'value'),
)
def update_output(value):
    if value == 'o_1':
        return {'visibility':'visible', 'margin-top':'5%','margin-left':'44%'}, \
                {'visibility':'hidden'}, \
                {'visibility':'hidden'}, \
                {'visibility':'hidden'}, \
                {}, ""
    
    if value == 'o_2':
        return {'visibility':'hidden'}, \
                {'visibility':'hidden'}, \
                {'visibility':'hidden'}, \
                {'visibility':'hidden'}, \
                {'margin-top':'-2%',
                'width': '27%',
                'margin-left': '35%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'visibility':'visible'}, \
                "Upload File"
    
    if value == 'o_3':
        return {'visibility':'hidden'}, \
                {'visibility':'visible','width':'10%','margin-top':'5%','margin-left':'20%'}, \
                {'visibility':'visible','width':'10%','margin-left':'5%'}, \
                {'visibility':'visible', 'margin-left':'5%'}, \
                {}, ""
    
    return {'visibility':'hidden'}, \
            {'visibility':'hidden'}, \
            {'visibility':'hidden'}, \
            {'visibility':'hidden'}, \
            {}, ""

# in this callback on base, what buttons and inputs was set call ann functions. 
@app.callback(
    Output('graph', 'figure'),
    Output('output-data-upload', 'children'),
    Output('info','children'),
    
    Input('init','n_clicks'),
    Input('reset','n_clicks'),
    Input('elipse','n_clicks'),
    Input('aprox','n_clicks'),

    Input('b_test','n_clicks'),
    Input('b_train','n_clicks'),
    Input('upload-data', 'contents'),
    
    State('x1', 'value'),
    State('x2', 'value'),
    State('upload-data', 'filename'),
    )
def update_output(btn0, btn1, btn2, btn3, btn4, btn5, list_of_contents, input1, input2, name):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'b_train' in changed_id:
        test_acc, test_loss = ann.train_net()
        return ann.graph.fig, "", "[INFO] Trained ann! Test accuracy:" + str(test_acc) + " Test loss function: " + str(test_loss)

    elif 'b_test' in changed_id:
        ann.write = 'a+'

        # catching exception as text or out range number,
        # also can be add point with ./,  
        try:
            input1 = float(input1.replace(',' , '.'))
            input2 = float(input2.replace(',' , '.'))
            
            if ((input1 > -4 and input1 < 2) and (input2 > 2 and input2 < 5)):
                ann.net_sp([[input1, input2]])
                return ann.graph.fig, "", "[INFO] Point " + str([input1,input2]) + " has been processed!"
            
            else:
                return ann.graph.fig, "", "[INFO] Inputs out of range!"

        except ValueError:
            return ann.graph.fig, "", "[INFO] That was no valid number!"

    elif 'reset' in changed_id:
        ann.reset()
        return ann.graph.fig, "", "[INFO] Reset Graph!"
    
    elif 'init' in changed_id:
        ann.net_gp()
        return ann.graph.fig, "", "[INFO] Init classificator!"
    
    elif 'elipse' in changed_id:
        ann.elipse()
        return ann.graph.fig, "", "[INFO] Elipse by equation!"
    
    elif 'aprox' in changed_id:
        ann.approx_bound()
        return ann.graph.fig, "", "[INFO] Aproximated elipse by classificator!"

    else:
        if name is not None:
            ann.write = 'w'
            points = []

            with open(name, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                
                # catching exception as text or out range number,
                # also can be add point with ./,  
                try:
                    for i in reader:
                        points.append([float(i[0].replace(',' , '.')), float(i[1].replace(',' , '.'))]), 

                except ValueError:
                    return ann.graph.fig, "", "[INFO] In file is no valid number!"

            for i in points:
                if not ((i[0] > -4 and i[0] < 2) and (i[1] > 2 and i[1] < 5)):
                    return ann.graph.fig, "", "[INFO] In file: " + name + ". Point in line " + str(points.index(i)+1) + " is out of range!"
            
            ann.filename = name
            ann.net_sp(points)
            return ann.graph.fig, "", "[INFO] File " + name + " was uploaded!"
            
    return fig, "", "- INFO -"

if __name__ == '__main__':
    # only error outputs
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    # run local server
    app.run_server(
        host='127.0.0.1', 
        port='14508',
        debug=False,
    )