import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd


def PPV(V,D,P):
    ppv = V*D / (V*D + (100-D)*(100-P))
    #print(ppv)
    return ppv

def NPV(V,D,P):
    npv = P*(100-D) / (P*(100-D)+D*(100-V))
    return npv


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    #html.H1('PPV and NPV'),

    dcc.Graph(id='indicator-graphic'),

    html.Label('Prevalence', id='Prevalence-label'),
    dcc.Slider(
        id='prev--slider',
        min=0,
        max=100,
        value=22,
        marks={str(per): "" for per in np.arange(0,100,0.1)},
        step=None,
        updatemode='drag',
    ),

    html.Label('Sensitivity', id='Sensitivity-label'),
    dcc.Slider(
        id='sensi--slider',
        min=0,
        max=100,
        value=75,
        marks={str(per): "" for per in np.arange(0,100,0.1)},
        step=None,
        updatemode='drag'
    ),

    html.Label('Specificity', id='Specificity-label'),
    dcc.Slider(
        id='speci--slider',
        min=0,
        max=100,
        value=75,
        marks={str(per): "" for per in np.arange(0,100,0.1)},
        step=10,
        updatemode='drag'
    )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('prev--slider', 'value'),
     Input('sensi--slider', 'value'),
     Input('speci--slider', 'value')
     ])
def update_graph(prev_value,sensi_value,speci_value):
    xaxis_column_name = "Number of People"
    xaxis_type = "Linear"
    yaxis_column_name = 'Arbitrary'
    yaxis_type = 'Linear'

    set_Sensitivity = sensi_value/100
    set_Specificity = speci_value/100
    set_Prevalence = prev_value/100
    pop_size = 100


    speci = set_Specificity
    sensi = set_Sensitivity
    preva = set_Prevalence
    scaler = 2
    healthy = pop_size*(1-preva)
    sick = pop_size*preva
    numSickPos = round(sensi*sick)
    numSickNeg = sick - numSickPos
    numHealthyNeg = round(speci*healthy)
    numHealthyPos = healthy - numHealthyNeg

    pop1 = np.arange(0,numSickPos,1)
    pop2 = np.arange(numSickPos,sick,1)
    pop3 = np.arange(sick,sick+numHealthyPos,1)
    pop4 = np.arange(sick+numHealthyPos,pop_size,1)

    neg1 = np.arange(0,numHealthyNeg,1)
    neg2 = np.arange(numHealthyNeg,numHealthyNeg+numSickNeg,1)

    pos1 = np.arange(0,numSickPos,1)
    pos2 = np.arange(numSickPos,numSickPos+numHealthyPos,1)

    ppv = PPV(sensi*100,preva*100,speci*100)*100
    npv = NPV(sensi*100,preva*100,speci*100)*100

    return {
        'data': [dict(
            x = np.concatenate([pop1,pos1]),
            y = np.concatenate([np.ones(len(pop1)),3*np.ones(len(pos1))]),
            mode='markers',
            marker=dict(
                size=16,
                color='red', #set color equal to a variable
                #colorscale='Viridis', # one of plotly colorscales
                #showscale=True
            ),
            name="Sick, Positive"
        ), dict(
            x = np.concatenate([pop2,neg2]),
            y = np.concatenate([np.ones(len(pop2)),2*np.ones(len(neg2))]),
            mode='markers',
            marker=dict(
                size=16,
                color='orange', #set color equal to a variable
                #colorscale='Viridis', # one of plotly colorscales
                #showscale=True
            ),
            name="Sick, Negative"
        ), dict(
            x = np.concatenate([pop3,pos2]),
            y = np.concatenate([np.ones(len(pop3)),3*np.ones(len(pos2))]),
            mode='markers',
            marker=dict(
                size=16,
                color='blue', #set color equal to a variable
                #colorscale='Viridis', # one of plotly colorscales
                #showscale=True
            ),
            name="Healthy, Positive"
        ), dict(
                x = np.concatenate([pop4,neg1]),
                y = np.concatenate([np.ones(len(pop4)),2*np.ones(len(neg1))]),
                mode='markers',
                marker=dict(
                    size=16,
                    color='green', #set color equal to a variable
                    #colorscale='Viridis', # one of plotly colorscales
                    #showscale=True
                ),
                name="Healthy, Negative"
        ), dict(
                x=[20, 20],
                y=[1.75, 2.75],
                mode="text",
                #name="Lines, Markers and Text",
                text=["NPV: {: 2.0f}%".format(npv), "PPV: {: 2.0f}%".format(ppv)],
                textfont=dict(
                    family="Georgia",
                    size=16,
                    color="black"
                    ),
                textposition="top center",
                showlegend=False
        ), dict(
                x=[96,96,96],
                y=[2.5,2.01,3.01],
                mode="text",
                #name="Lines, Markers and Text",
                text=["Sensitivity: {: 2.0f}%".format(sensi*100),
                      "Specificity: {: 2.0f}%".format(speci*100),
                      "Prevalence: {: 2.0f}%".format(preva*100),
                      ],
                textfont=dict(
                    family="Georgia",
                    size=16,
                    color="black"
                    ),
                textposition="top center",
                showlegend=False
        ), dict(
                x=[5,6,6],
                y=[1.15,2.15,3.15],
                mode="text",
                #name="Lines, Markers and Text",
                text=["Population",
                      "Negative Tests",
                      "Positive Tests",
                      ],
                textfont=dict(
                    family="Georgia",
                    size=18,
                    color="black"
                    ),
                textposition="top center",
                showlegend=False
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'range': [0,4],
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log',
                'visible' : False
            },
            margin={'l': 20, 'b': 40, 't': 10, 'r': 20},
            hovermode='y'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
