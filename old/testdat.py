import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
np.random.seed(0)
z1, z2, z3 = np.random.random((3, 7, 7))
print(type(z2))
fig = go.Heatmap(
    z=z1,
    customdata=np.dstack((z2, z3)),
    hovertemplate='<b>z1:%{z:.3f}</b><br>z2:%{customdata[0]:.3f} <br>z3: %{customdata[1]:.3f} ',
    coloraxis="coloraxis1", name='')

fig.show()
