import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import numpy as np
from datetime import datetime
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
df = pd.read_csv("datasets/test-dataset.csv")
#df = pd.read_csv("datasets/openpowerlifting-2020-05-10.csv")

#df = pd.read_csv("https://media.githubusercontent.com/media/robertej19/powerlifting/master/datasets/test-dataset.csv")

#print("reading datafile")
#df = pd.read_csv("https://media.githubusercontent.com/media/robertej19/powerlifting/master/datasets/openpowerlifting-2020-05-10.csv")
#for item in df:
#    print(item)
#    print(df[item])

print("data reading finished")

Sex = ['M','F']
Sex_Values = ['Male','Female']
m_weightclasses = [59, 66, 74, 83, 93, 105, 120,130]
f_weighclasses = [47, 52, 57, 63, 72, 84,100]

wclasses =[m_weightclasses,f_weighclasses]

#deadlifts = []

deadlifts = []
deadlifts_labels = []
deadlifts_hist_data = []
squats = []
squats_labels = []
squats_hist_data = []
bench = []
bench_labels = []
bench_hist_data = []

for sex_ind,sex in enumerate(Sex):
    deadlifts.append([])
    squats.append([])
    bench.append([])
    deadlifts_labels.append([])
    squats_labels.append([])
    bench_labels.append([])
    deadlifts_hist_data.append([])
    squats_hist_data.append([])
    bench_hist_data.append([])
    weightclass = wclasses[sex_ind]
    for weight in weightclass:
        deadlifts[sex_ind].append([])
        squats[sex_ind].append([])
        bench[sex_ind].append([])
        deadlifts_labels[sex_ind].append([])
        squats_labels[sex_ind].append([])
        bench_labels[sex_ind].append([])
        deadlifts_hist_data[sex_ind].append([])
        squats_hist_data[sex_ind].append([])
        bench_hist_data[sex_ind].append([])

print("sorting data")


for ind in df.index:
    if ind % 10000 == 0:
        print(ind)
    person_sex = df['Sex'][ind]
    person_weight = df['BodyweightKg'][ind]
    best_dl = df['Best3DeadliftKg'][ind]
    best_squat = df['Best3SquatKg'][ind]
    best_bench = df['Best3BenchKg'][ind]



    if person_sex in Sex:
        sex_ind = Sex.index(person_sex)
        weightclass = wclasses[sex_ind]

        #print("max weight")
        #print(weightclass[len(weightclass)-2])
        if person_weight > weightclass[len(weightclass)-2]:
            weight_class = weightclass[len(weightclass)-1]
            weight_ind = weightclass.index(weight_class)
        else:
            for test_weight_ind, weight in enumerate(weightclass):
                if person_weight < weight:
                    weight_class= weight
                    weight_ind = test_weight_ind
                    break

        if weight_class in weightclass:
                deadlifts[sex_ind][weight_ind].append(best_dl)
                squats[sex_ind][weight_ind].append(best_squat)
                bench[sex_ind][weight_ind].append(best_bench)

        else:
            print("weight is {}, sex is {}".format(person_weight,person_sex))
            print("sex ind is {}, weight ind is {}".format(sex_ind,weight_ind))
    else:
        print("weight is {}, sex is {}".format(person_weight,person_sex))
        print("sex ind is {}, weight ind is {}".format(sex_ind,weight_ind))

Lift_Values = ['Squat','Bench','Deadlift']
lifts = [squats,bench,deadlifts]
lifts_labels = [squats_labels,bench_labels,deadlifts_labels]
lifts_hist_data = [squats_hist_data,bench_hist_data,deadlifts_hist_data]


print("generating hist data")

for lift_ind,lift_type in enumerate(lifts):
    for sex_ind,sex in enumerate(Sex):
        weightclass = wclasses[sex_ind]
        for weight_ind,weight in enumerate(weightclass):

            lift_data = lifts[lift_ind][sex_ind][weight_ind]
            lift_counts, hist_bins = np.histogram(lift_data, bins=100, range=(0, 500))

            #print(lift_ind,sex_ind,weight_ind)
            lifts_hist_data[lift_ind][sex_ind][weight_ind] = lift_counts

            num_lifters_total = sum(lift_counts) #get total number of lifters in weightclass

            for ind, bin_val in enumerate(hist_bins):
                num_better = sum(lift_counts[(ind+1):])
                frac = num_better/num_lifters_total*100 #to make it a percent
                lifts_labels[lift_ind][sex_ind][weight_ind].append(frac)



    #print(person_weight,weight_class)



#print(deadlifts[0][4])

#    if person_sex == Sex[0]:
#        if person_weight in range(20,120):
#            deadlifts.append()

"""
for sexi_ind,sexi in enumerate(Sex):
    weightclass = wclasses[sex_ind]
    for weight_ind,weight in enumerate(weightclass):
"""






    #print(df['BodyweightKg'][ind])
    #print(df['Best3DeadliftKg'][ind])

print("datasorting finished")

#print(deadlifts)


#deadlifts = ['nan', 88.45, 127.01, 131.54, 142.88, 104.33, 104.33, 63.5, 162.5]


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

            html.Div([
                dcc.RadioItems(
                    id='sex-type',
                    options=[{'label': i, 'value': i} for i in Sex_Values],
                    value=Sex_Values[1],
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),


            html.Div([
                dcc.RadioItems(
                    id='lift-type',
                    options=[{'label': i, 'value': i} for i in Lift_Values],
                    value=Lift_Values[2],
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),



    dcc.Graph(id='indicator-graphic'),

    html.Div(
    dcc.Slider(
        id='male-year--slider',
        min=min(wclasses[0]),
        max=max(wclasses[0]),
        value=wclasses[0][wclasses[0].index(min(wclasses[0]))+2],
        marks={str(year): str(year) for year in wclasses[0]},
        step=None,
        updatemode='drag',
    ), id='malesliderContainer'),

    html.Div(
    dcc.Slider(
        id='female-year--slider',
        min=min(wclasses[1]),
        max=max(wclasses[1]),
        value=wclasses[1][wclasses[1].index(min(wclasses[1]))+2],
        marks={str(year): str(year) for year in wclasses[1]},
        step=None,
        updatemode='drag',
    ), id='femalesliderContainer')



])
])



@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('sex-type', 'value'),
    Input('lift-type', 'value'),
    Input('female-year--slider', 'value'),
    Input('male-year--slider', 'value')])
def update_graph(sex_val,lift_val,fe_year_value,male_year_value):


    #print(sex_val)

    if Sex_Values.index(sex_val)==0:
        year_value = male_year_value
    else:
        year_value = fe_year_value

    #print(year_value)
    #print(lift_val)

    #lift_set = lifts[Lift_Values.index(lift_val)]

    #print(lift_set)

    sex_ind = Sex_Values.index(sex_val)
    weight_ind = wclasses[Sex_Values.index(sex_val)].index(year_value)
    lift_ind = Lift_Values.index(lift_val)
    #hist_data = lift_set[Sex_Values.index(sex_val)][wclasses[Sex_Values.index(sex_val)].index(year_value)]


    hist_x_data = hist_bins
    hist_y_data = lifts_hist_data[lift_ind][sex_ind][weight_ind]
    hist_hover_labels = lifts_labels[lift_ind][sex_ind][weight_ind]
    #print(hist_hover_labels)

    fig10 = {
        'data': [go.Bar(x=hist_x_data, y=hist_y_data,
                hovertemplate =
                '<b>Weight: %{x:.2f} kg, %{x*2.024:.2f} lbs </b>: %{x}<br>'+
                '<br><b>Percent of Lifters Above This</b>: %{text:.2f} %',
                text = hist_hover_labels),
                       #hovertext=hist_hover_labels)
            ],
        'layout': dict(
            xaxis={
                'range': [50,450],
                'title': 'Deadlift Weight (kg)',
                'textfont' : dict(
                    family="Georgia",
                    size=36,
                    #color="#7f7f7f"
                )
            },
            yaxis={
                'title': "Number of Lifters"
            },

            #hovertext=["Text A", "Text B", "Text C", "Text D", "Text E"],
            #hoverinfo="text",
            margin={'l': 100, 'b': 40, 't': 10, 'r': 20},
            #hovermode='x unified',
            bargap=0.1, # gap between bars of adjacent location coordinates
            bargroupgap=0.1 # gap between bars of the same location coordinates
        )
    }

    return fig10



@app.callback(Output('malesliderContainer', 'style'),
    [Input('sex-type', 'value')])
def update_slide(sex_val):

    ind = Sex_Values.index(sex_val)

    if ind == 0:
        return {}
    else:
        return {'display': 'none'}



@app.callback(Output('femalesliderContainer', 'style'),
    [Input('sex-type', 'value')])
def update_slide(sex_val):

    ind = Sex_Values.index(sex_val)

    if ind == 1:
        return {}
    else:
        return {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)
