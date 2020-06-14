import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import numpy as np

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
df = pd.read_csv("datasets/test-dataset.csv")
#df = pd.read_csv("https://media.githubusercontent.com/media/robertej19/powerlifting/master/datasets/test-dataset.csv")

#df = pd.read_csv("https://media.githubusercontent.com/media/robertej19/powerlifting/master/datasets/openpowerlifting-2020-05-10.csv")
#for item in df:
#    print(item)
#    print(df[item])

Sex = 'M'
deadlifts = []

for ind in df.index:
    #print(item[ind])
    if df['Sex'][ind] == Sex:
        if (df['BodyweightKg'][ind]) in range(74,93):
            deadlifts.append(df['Best3DeadliftKg'][ind])

    #print(df['BodyweightKg'][ind])
    #print(df['Best3DeadliftKg'][ind])

print(deadlifts)

m_weightclasses = [59, 66, 74, 83, 93, 105, 120]
w_weighclasses = [47, 52, 57, 63, 72, 84]
#available_indicators = df['Indicator Name'].unique()



fig = go.Figure(data=[go.Histogram(x=deadlifts)])

fig.show()


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
