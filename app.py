import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

from flask import Flask, render_template

app = Flask(__name__)
data_df = pd.read_csv('matches_csv/testmatch.csv')


@app.route('/')
def index():
    bar = create_plot()
    return render_template('index.html', plot=bar)

@app.route('/data')
def data():
    return '<h1> DATA E COOLT</h1>'

def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.read_csv('./matches_csv/testmatch.csv', sep=';') # creating a sample dataframe
    # df = df[(df['player name'] == 'Kuzon')]

    data = [
        go.Bar(
            x=df['player name'], # assign x as the dataframe column 'x'
            y=df['assists']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
