import plotly.express as px
import pandas as pd
import numpy as np

y_name = input("y name: ")
X_name = 'X_pca.txt'

if y_name == '1':
    y_name = 'y_sliding.txt'
    print("Showing y_sliding.txt")
elif y_name == '2':
    y_name = 'y_kmeans.txt'
    print("Showing y_kmeans.txt")
else:
    print("Invalid value")


X = np.loadtxt(X_name)
colors = np.loadtxt(y_name)

df = pd.DataFrame(X, columns=['x', 'y', 'z'])
df['Color'] = colors

fig = px.scatter_3d(df, x='x', y='y', z='z', color='Color', opacity=1, size_max=8)
fig.update_traces(marker=dict(size=3))
fig.show()

