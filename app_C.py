import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json
import sys

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

    numberofmatches = 2
    allmatches = {}
    allmatches_CK = {}
    kuzon = {}
    sneaky = {}
    #listofzeros = [0] * numberofmatches
    #sneaky['totalspeed'], sneaky['totalboost'], sneaky['totalassist'], sneaky['totalscore'], sneaky['totalgoals'] = listofzeros
    #kuzon['totalspeed'], kuzon['totalboost'], kuzon['totalassist'], kuzon['totalscore'], kuzon['totalgoals'] = listofzeros
    sneakytotalspeed = 0
    kuzontotalspeed = 0
    sneakytotalscore = 0
    kuzontotalscore = 0
    for i in range(0, numberofmatches):
        tempmatch = pd.read_csv('./matches_csv/testmatch' + str(i) + '.csv', sep=';')
        kuzon = tempmatch[tempmatch['player name'].str.contains('Kuzon')]
        sneaky = tempmatch[tempmatch['player name'].str.contains('Sneakyb4stard')]
        allmatches[i] = tempmatch
        #kuzon = kuzon.to_numpy()
        #sneaky = sneaky.to_numpy()
        kuzontotalspeed += kuzon['avg speed'].values
        sneakytotalspeed += sneaky['avg speed'].values
        sneakytotalscore += sneaky['score'].values
        kuzontotalscore += kuzon['score'].values


        frames = [kuzon, sneaky]
        allmatches_CK[i] = pd.concat(frames)


    sneakyaveragespeed = average(sneakytotalspeed, numberofmatches)
    kuzonaveragespeed = average(kuzontotalspeed, numberofmatches)
    Sneakyaveragescore = average(sneakytotalscore, numberofmatches)
    kuzonaveragescore = average(kuzontotalscore, numberofmatches)
    print('Sneakyaveragespeed: ' + str(sneakyaveragespeed) + ' kuzonaveragespeed: ' + str(kuzonaveragespeed), file=sys.stderr)

    #playerdata[0] = kuzon;
    #playerdata[1] = sneaky;

    #df = pd.read_csv('./matches_csv/testmatch1.csv', sep=';') # creating a sample dataframe
    # df = df[(df['player name'] == 'Kuzon')]

    
    if "match1" in request.form:
        data = [
        go.Bar(
            name = "speed" + str(1),
            x=allmatches_CK[1]['player name'], # assign x as the dataframe column 'x'
            y=allmatches_CK[1]['avg speed']

        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index_C.html', plot=graphJSON)
        #return graphJSON 
    elif "match2" in request.form:
        data = [
        go.Bar(
            x=allmatches[1]['player name'], # assign x as the dataframe column 'x'
            y=allmatches[1]['avg speed']
        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)   
        return render_template('index_C.html', plot=graphJSON)
        #return graphJSON
    else:
        data = [
        go.Bar(
            #x=allmatches[0]['player name'], # assign x as the dataframe column 'x'
            #y=allmatches[0]['score']
            x = allmatches_CK[0]['player name'],
            y = allmatches_CK[0]['avg speed']
        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)   
        return render_template('index_C.html', plot=graphJSON)
        #return graphJSON

    #graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    #return graphJSON

def average(var, n):
    return var/n
    
if __name__ == '__main__':
    app.run(debug=True)
