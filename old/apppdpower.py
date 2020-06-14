import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import numpy as np
from collections import Counter
from datetime import datetime
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

"""
#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
df = pd.read_csv("datasets/test-dataset.csv")

#df = pd.read_csv("https://media.githubusercontent.com/media/robertej19/powerlifting/master/datasets/test-dataset.csv")

#print("reading datafile")
#df = pd.read_csv("https://media.githubusercontent.com/media/robertej19/powerlifting/master/datasets/openpowerlifting-2020-05-10.csv")
#for item in df:
#    print(item)
#    print(df[item])

print("data reading finished")

Sex = 'F'
deadlifts = []

print("sorting data")
for ind in df.index:
    #print(item[ind])
    if df['Sex'][ind] == Sex:
        if (df['BodyweightKg'][ind]) in range(20,120):
            deadlifts.append(df['Best3DeadliftKg'][ind])

    #print(df['BodyweightKg'][ind])
    #print(df['Best3DeadliftKg'][ind])

print("datasorting finished")

"""
#print(deadlifts)


deadlifts = ['nan', 88.45, 127.01, 131.54, 142.88, 104.33, 104.33, 63.5, 162.5]

m_weightclasses = [59, 66, 74, 83, 93, 105, 120]
w_weighclasses = [47, 52, 57, 63, 72, 84]
#available_indicators = df['Indicator Name'].unique()


"""
International Powerlifting Federation (IPF) weight classes:
Women: 47 kg, 52 kg, 57 kg, 63 kg, 72 kg, 84 kg, 84 kg+
Men: 59 kg, 66 kg, 74 kg, 83 kg, 93 kg, 105 kg, 120 kg, 120 kg+
Sex
equipment
age
age class
bodyweight
weightclass
Best3SquatKg
Best3BenchKg
Best3DeadliftKg
TotalKg

--- analytics of powerlifting ---
Dots
Wilks
Glossbrenner
Goodlift

make a histogram - male, weightclass, distro of deadlifts

"""

app.layout = html.Div([
    html.Div([

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        #marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
])
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('year--slider', 'value')])
def update_graph(year_value):

    return {
        'data': [go.Histogram(x=deadlifts,
                xbins=dict( # bins used for histogram
                start=-4.0,
                end=500.0,
                size=5
            ),
            )],
        'layout': dict(
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
            title_text='Sampled Results', # title of plot
            xaxis_title_text='Value', # xaxis label
            yaxis_title_text='Count', # yaxis label
            bargap=0.1, # gap between bars of adjacent location coordinates
            bargroupgap=0.1 # gap between bars of the same location coordinates
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
