import plotly.graph_objects as go
import numpy as np
from plotly.graph_objects import *



def PPV(V,D,P):
    ppv = V*D / (V*D + (100-D)*(100-P))
    #print(ppv)
    return ppv

def NPV(V,D,P):
    npv = P*(100-D) / (P*(100-D)+D*(100-V))
    return npv

# Create figure
fig = go.Figure()

file_type = "Prevalence"


# Add traces, one for each slider step

set_Sensitivity = 0.82
set_Specificity = 0.88
set_Prevalence = 0.2


#Total number of people
fig.add_trace(go.Scatter(
    visible = True,
    x = np.arange(0,100,1),
    y = np.ones(100),
    mode='markers',
    marker=dict(
        size=16,
        color='black', #set color equal to a variable
        #colorscale='Viridis', # one of plotly colorscales
        #showscale=True
    ),
    name="Healthy",
    showlegend=False
))

for sicki100 in np.arange(0, 100, 1):
    speci = set_Specificity
    sense = set_Sensitivity
    sick = sicki100
    scaler = 2
    healthy = 100 - sick
    numSickPos = round(sense*sick)
    numSickNeg = sick - numSickPos
    numHealthyPos = round((1-speci)*healthy)
    numHealthyNeg = healthy - numHealthyPos

    x = np.arange(0,sick,1)

    #Total number of sick people
    fig.add_trace(go.Scatter(
        visible = False,
        x = x,
        y = np.ones(len(x)),
        mode='markers',
        marker=dict(
            size=16,
            color='pink', #set color equal to a variable
            #colorscale='Viridis', # one of plotly colorscales
            #showscale=True
        ),
        #name="Sick, Positive"
        showlegend = False,
        opacity=0
    ))



    x = np.arange(0,numSickPos,1)
    #Number of sick people testing positive
    fig.add_trace(go.Scatter(
        visible = False,
        x = np.concatenate([x,x]),
        y = np.concatenate([3*np.ones(len(x)),np.ones(len(x))]),
        mode='markers',
        marker=dict(
            size=16,
            color='red', #set color equal to a variable
            #colorscale='Viridis', # one of plotly colorscales
            #showscale=True
        ),
        name="Sick, Positive"
    ))

    x = np.arange(numHealthyNeg,numHealthyNeg+numSickNeg,1)
    xz = np.arange(numSickPos,numSickPos+numSickNeg,1)
    #Number of sick people testing negative
    fig.add_trace(go.Scatter(
        visible = False,
        x = np.concatenate([x,xz]),
        y = np.concatenate([2*np.ones(len(x)),np.ones(len(x))]),
        mode='markers',
        marker=dict(
            size=16,
            color='orange', #set color equal to a variable
            #colorscale='Viridis', # one of plotly colorscales
            #showscale=True
        ),
        name="Sick, Negative"
    ))


    x = np.arange(numSickPos,numSickPos + numHealthyPos,1)
    #Number of sick people testing positive
    xz = np.arange(numSickPos+numSickNeg,100-numHealthyNeg,1)
    fig.add_trace(go.Scatter(
        visible = False,
        x = np.concatenate([x,xz]),
        y = np.concatenate([3*np.ones(len(x)),np.ones(len(x))]),
        mode='markers',
        marker=dict(
            size=16,
            color='blue', #set color equal to a variable
            #colorscale='Viridis', # one of plotly colorscales
            #showscale=True
        ),
        name="Healthy, Positive"
    ))

    #print(healthy)
    x = np.arange(0,numHealthyNeg,1)
    #Number of sick people testing negatvie
    xz = np.arange(100-numHealthyNeg,100,1)
    fig.add_trace(go.Scatter(
        visible = False,
        x = np.concatenate([x,xz]),
        y = np.concatenate([2*np.ones(len(x)),np.ones(len(x))]),
        mode='markers',
        marker=dict(
            size=16,
            color='green', #set color equal to a variable
            #colorscale='Viridis', # one of plotly colorscales
            #showscale=True
        ),
        name="Healthy, Negative"
    ))


    ppv = PPV(sense*100,sick,speci*100)*100
    npv = NPV(sense*100,sick,speci*100)*100
    fig.add_trace(go.Scatter(
        visible = False,
        x=[20, 20],
        y=[1.8, 2.8],
        mode="text",
        #name="Lines, Markers and Text",
        text=["NPV: {: 2.0f}%".format(npv), "PPV: {: 2.0f}%".format(ppv)],
        textfont=dict(
            family="Courier New, monospace",
            size=14,
            color="black"
            ),
        textposition="top center",
        showlegend=False
    ))


fig.update_xaxes(range=[-1,100])



"""
# Create and add slider
steps = []
for j in range(int(int(len(fig.data)-1)/5)):
    i = j*5
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Disease Prevalence: " + str(j) + "%"}],  # layout attribute
    )
    step["args"][0]["visible"][0] = True
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    step["args"][0]["visible"][i-1] = True
    step["args"][0]["visible"][i-2] = True  # Toggle i'th trace to "visible"
    step["args"][0]["visible"][i-3] = True
    step["args"][0]["visible"][i-4] = True
    steps.append(step)
    #step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    #steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

"""




fig.update_yaxes({
    'range': [0, 4],
    'showgrid': False, # thin lines in the background
    'zeroline': False, # thick line at x=0
    'visible': False,  # numbers below
}) # the same for yaxis

"""
fig.update_xaxes({
    'range': [1.4, 2.6],
    'showgrid': False, # thin lines in the background
    'zeroline': False, # thick line at x=0
    'visible': False,  # numbers below
}) # the same for yaxis

"""

# Make 10th trace visible
#fig.data[0].visible = True
#fig.data[11].visible = True
#fig.data[12].visible = True
#fig.data[13].visible = True


# Create and add slider
steps = []
for j in range(int(int(len(fig.data)-1)/6)):
    i = j*6
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "{}: {}%".format(file_type,j)}],  # layout attribute
    )
    step["args"][0]["visible"][0] = True
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    step["args"][0]["visible"][i-1] = True
    step["args"][0]["visible"][i-2] = True  # Toggle i'th trace to "visible"
    step["args"][0]["visible"][i-3] = True
    step["args"][0]["visible"][i-4] = True
    step["args"][0]["visible"][i-5] = True
    #step["args"][0]["visible"][i-4] = True
    steps.append(step)
    #step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    #steps.append(step)


sliders = [dict(
    active=32,
    currentvalue={"prefix": "{}: ".format(file_type)},
    pad={"t": 50},
    steps=steps,
    tickcolor='white',
    font={'color': 'white'}
)]

fig.data[180].visible = True
fig.data[181].visible = True
fig.data[182].visible = True
fig.data[183].visible = True
fig.data[184].visible = True
fig.data[185].visible = True



fig.add_annotation(
        x=10,
        y=3.5,
        #xref="x",
        #yref="y",
        text="Specificity: {: 2.0f}%".format(set_Specificity*100),
        #showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="black"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="rgba(0,0,0,0)",
        #ax=20,
        #ay=-30,
        bordercolor="white",
        borderwidth=2,
        borderpad=4,
        bgcolor="white",
        opacity=1
        )

fig.add_annotation(
        x=40,
        y=3.5,
        #xref="x",
        #yref="y",
        text="Sensitivity: {: 2.0f}%".format(set_Sensitivity*100),
        #showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="black"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="rgba(0,0,0,0)",
        #ax=20,
        #ay=-30,
        bordercolor="white",
        borderwidth=2,
        borderpad=4,
        bgcolor="white",
        opacity=1
        )

fig.add_annotation(
        x=5,
        y=3.1,
        #xref="x",
        #yref="y",
        text=("Positive Tests"),
        #showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="black"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="rgba(0,0,0,0)",
        #ax=20,
        #ay=-30,
        bordercolor="white",
        borderwidth=2,
        borderpad=4,
        bgcolor="white",
        opacity=1
        )


fig.add_annotation(
        x=5,
        y=2.1,
        #xref="x",
        #yref="y",
        text=("Negative Tests"),
        #showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="black"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="rgba(0,0,0,0)",
        #ax=20,
        #ay=-30,
        bordercolor="white",
        borderwidth=2,
        borderpad=4,
        bgcolor="white",
        opacity=1
        )



layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


fig.update_layout({'paper_bgcolor':'rgba(0,0,0,0)', 'plot_bgcolor':'rgba(0,0,0,0)'})

fig.update_layout(
    sliders=sliders
)

fig.update_layout(title={'text':'{}: 32%'.format(file_type),'x':0.5,'xanchor':'center'})



























import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)  # Turn off reloader if inside Jupyter
