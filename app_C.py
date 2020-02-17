import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json
import sys

from flask import Flask, render_template
from flask import request
app = Flask(__name__)

numberofmatches = 2
allmatches = {}
allmatches_CK = {}
allmatches_CK_wins = {}
allmatches_CK_losses = {}
kuzon = {}
sneaky = {}

#@app.route('/')
#def index():
    

@app.route('/data')
def data():
    return '<h1> DATA E COOLT</h1>'



@app.route('/', methods=["GET", "POST"])
def index():
    #bar = create_plot()
    read_data()
    return create_plot2()
    #return render_template('index.html', plot=bar)
def create_plot2():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    
    #go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
    #go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
    df = pd.DataFrame(allmatches_CK_wins[0])
    #kuzon = allmatches_CK_losses[allmatches_CK_losses['player name'].str.contains('Kuzon')]
    #sneaky = allmatches_CK_wins[allmatches_CK_wins['player name'].str.contains('Sneakyb4stard')]

    if "wins" in request.form:
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']
        #sneaky = allmatches_CK_wins[allmatches_CK_wins['player name'] == 'Sneakyb4stard']
        sneaky = df[df['player name'] == 'Sneakyb4stard']
        kuzon = df[df['player name'] == 'Kuzon']

        print('test output: ' + str(allmatches_CK_wins[0]['percentage boost speed']), file=sys.stderr)

        print('test output 2: ' + str(sneaky['percentage supersonic speed'].values) + 'kuzon: ' + str(kuzon['percentage supersonic speed'].values))
        
        fig = go.Figure(data = [
        go.Bar(
            name = "sneaky" + str(1),
            x = xdata,
            #y=[18, 15, 20]
            y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,
            
            
        ),
        go.Bar(
            name = "kuzon",
            x = xdata,
            #y=[18, 15, 20]
            y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            )
        ])
        fig.update_layout(barmode='group')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index_C.html', plot=graphJSON)
        #return graphJSON 
    elif "losses" in request.form:
        data = [
        go.Bar(
            x=allmatches_CK_losses[0]['player name'], # assign x as the dataframe column 'x'
            y=allmatches_CK_losses[0]['goals']
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
            y = allmatches_CK[0]['goals']
        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)   
        return render_template('index_C.html', plot=graphJSON)

def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    
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


def read_data():

     #listofzeros = [0] * numberofmatches
    #sneaky['totalspeed'], sneaky['totalboost'], sneaky['totalassist'], sneaky['totalscore'], sneaky['totalgoals'] = listofzeros
    #kuzon['totalspeed'], kuzon['totalboost'], kuzon['totalassist'], kuzon['totalscore'], kuzon['totalgoals'] = listofzeros
    sneakytotalspeed = 0
    kuzontotalspeed = 0
    sneakytotalscore = 0
    kuzontotalscore = 0
    countlosses = 0
    countwins = 0
    for i in range(0, numberofmatches):
        tempmatch = pd.read_csv('./matches_csv/testmatch' + str(i) + '.csv', sep=';')
        kuzon = tempmatch[tempmatch['player name'].str.contains('Kuzon')]
        sneaky = tempmatch[tempmatch['player name'].str.contains('Sneakyb4stard')]
        frames = [kuzon, sneaky]
        allmatches[i] = tempmatch
        #for i in range(0, tempmatch.length)
        print('test: ' + str(sneaky['color'].values), file=sys.stderr)
        if(sneaky['color'].values == 'blue'):
            otherteamgoals = tempmatch[tempmatch['color'].str.contains('orange')]

            #print('test2: ' + str(sneaky['goals conceded'].values), file=sys.stderr)
            #print('test3:' + str(max(otherteamgoals['goals conceded'].values)), file=sys.stderr)
            if(max(otherteamgoals['goals conceded'].values) < sneaky['goals conceded'].values):
                allmatches_CK_wins[countwins] = pd.concat(frames)
                countwins += 1
                #allmatches_CK_wins.append(pd.concat(frames), ignore_index = True)
            else:
                #allmatches_CK_wins.append(pd.concat(frames), ignore_index = True)
                allmatches_CK_losses[countlosses] = pd.concat(frames)
                countlosses += 1
        else:
            otherteamgoals = tempmatch[tempmatch['color'].str.contains('blue')]
            if(max(otherteamgoals['goals conceded'].values) < sneaky['goals conceded'].values):
                allmatches_CK_wins[countwins] = pd.concat(frames)
                countwins += 1
                #allmatches_CK_wins.append(pd.concat(frames), ignore_index = True)
            else:
                allmatches_CK_losses[countlosses] = pd.concat(frames)
                countlosses += 1
                #allmatches_CK_wins.append(pd.concat(frames), ignore_index = True)
        #if(kuzon['goals conceded'] < tempmatch)
        #kuzon = kuzon.to_numpy()
        #sneaky = sneaky.to_numpy()
        kuzontotalspeed += kuzon['avg speed'].values
        sneakytotalspeed += sneaky['avg speed'].values
        sneakytotalscore += sneaky['score'].values
        kuzontotalscore += kuzon['score'].values


        allmatches_CK[i] = pd.concat(frames)

    #end of forloop
    #allmatches_CK_losses.reset_index
    #allmatches_CK_wins.reset_index
    sneakyaveragespeed = average(sneakytotalspeed, numberofmatches)
    kuzonaveragespeed = average(kuzontotalspeed, numberofmatches)
    Sneakyaveragescore = average(sneakytotalscore, numberofmatches)
    kuzonaveragescore = average(kuzontotalscore, numberofmatches)
    print('Sneakyaveragespeed: ' + str(sneakyaveragespeed) + ' kuzonaveragespeed: ' + str(kuzonaveragespeed), file=sys.stderr)
    print('wins: ' + str(len(allmatches_CK_wins)) + "losses: " + str(len(allmatches_CK_losses)), file=sys.stderr)
    #playerdata[0] = kuzon;
    #playerdata[1] = sneaky;

    #df = pd.read_csv('./matches_csv/testmatch1.csv', sep=';') # creating a sample dataframe
    # df = df[(df['player name'] == 'Kuzon')]
    
if __name__ == '__main__':
    app.run(debug=True)
