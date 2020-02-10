import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

from flask import Flask, render_template
from flask import request
app = Flask(__name__)


#@app.route('/')
#def index():
    

@app.route('/data')
def data():
    return '<h1> DATA E COOLT</h1>'



@app.route('/', methods=["GET", "POST"])
def index():
    #bar = create_plot()
    return create_plot()
    #return render_template('index.html', plot=bar)

def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    allmatches = {};

    numberofmatches = 2;
    for i in range(0, numberofmatches):
        allmatches[i] = pd.read_csv('./matches_csv/testmatch' + str(i) + '.csv', sep=';')



    #df = pd.read_csv('./matches_csv/testmatch1.csv', sep=';') # creating a sample dataframe
    # df = df[(df['player name'] == 'Kuzon')]

    
    if "match1" in request.form:
        data = [
        go.Bar(
            x=allmatches[0]['player name'], # assign x as the dataframe column 'x'
            y=allmatches[0]['score']
        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index.html', plot=graphJSON)
        #return graphJSON 
    elif "match2" in request.form:
        data = [
        go.Bar(
            x=allmatches[1]['player name'], # assign x as the dataframe column 'x'
            y=allmatches[1]['score']
        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)   
        return render_template('index.html', plot=graphJSON)
        #return graphJSON
    else:
        data = [
        go.Bar(
            x=allmatches[0]['player name'], # assign x as the dataframe column 'x'
            y=allmatches[0]['score']
        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)   
        return render_template('index.html', plot=graphJSON)
        #return graphJSON

    #graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    #return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
