import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json
import sys

## todo, should fix better handling of allmatches arrays, taking mean and variance directly from them. Structuring up the splitting of data and filtering directly.
from flask import Flask, render_template
from flask import request
app = Flask(__name__)

numberofmatches = 10
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
   
    df_win = pd.concat(allmatches_CK_wins)
    sneaky1 = df_win[df_win['player name'] == 'Sneakyb4stard']
    df_lose = pd.concat(allmatches_CK_losses)
    sneaky2 = df_lose[df_lose['player name'] == 'Sneakyb4stard']
    #sneaky1 = pd.concat(allmatches_CK_wins['player name'].str.contains('Sneakyb4stard'))
    #sneaky2 = pd.concat(allmatches_CK_losses['player name'].str.contains('Sneakyb4stard'))
    
    df = pd.concat(allmatches_CK)
    #print('testmean' + str(sneaky1['score'].mean()), file=sys.stderr)
    print('sneaky1' + str(sneaky2['goals']), file=sys.stderr)
    #for i in range(0, numberofmatches):
        #print('testoutput' + str(allmatches_CK_wins[i]), file=sys.stderr)
    
    sneaky = df[df['player name'] == 'Sneakyb4stard']
    kuzon = df[df['player name'] == 'Kuzon']

    #sneakylastgame = pd.concat(allmatches_CK[0])
    #kuzonlastgame = pd.concat(allmatches_CK[0])
    #sneaky = sneaky1
    #kuzon = sneaky2
    
    #go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
    #go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
    #df = pd.DataFrame(allmatches_CK_wins[0])
    
    var1name = 'percentage supersonic speed'
    var2name = 'percentage boost speed'
    var3name = 'percentage slow speed'

    if "sneakyandkuzon" in request.form:
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']
        
        fig1 = go.Figure(data = [
        go.Bar(
            name = "Sneaky",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())]      
        ),
        go.Bar(
            name = "Kuzon",
            x = xdata,
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())]
            )
        ])
        fig1.update_layout(barmode='group')
        graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)   

        xdata2 = ['percentage defensive third', 'percentage neutral third', 'percentage offensive third']
        fig2 = go.Figure(data = [
        go.Bar(
            name = "sneaky",
            x = xdata2,
            #y=[18, 15, 20]
            y=[int(sneaky['percentage defensive third'].mean()), int(sneaky['percentage neutral third'].mean()), int(sneaky['percentage offensive third'].mean())]
            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,
            
            
        ),
        go.Bar(
            name = "kuzon",
            x = xdata2,
            #y=[18, 15, 20]
            y = [int(kuzon['percentage defensive third'].mean()), int(kuzon['percentage neutral third'].mean()), int(kuzon['percentage offensive third'].mean())]
            )
        ])
        fig2.update_layout(barmode='group')
        graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)   

        xdata3 = ['percentage on ground', 'percentage low in air', 'percentage high in air']
        fig3 = go.Figure(data = [
        go.Bar(
            name = "sneaky",
            x = xdata3,
            #y=[18, 15, 20]
            y=[int(sneaky['percentage on ground'].mean()), int(sneaky['percentage low in air'].mean()), int(sneaky['percentage high in air'].mean())]
            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,
            
            
        ),
        go.Bar(
            name = "kuzon",
            x = xdata3,
            #y=[18, 15, 20]
            y = [int(kuzon['percentage on ground'].mean()), int(kuzon['percentage low in air'].mean()), int(kuzon['percentage high in air'].mean())]
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3)
        #return graphJSON 
    elif "winsandlosses" in request.form:
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())]      
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())]
            )
        ])
        fig1.update_layout(barmode='group')
        graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)   

        #xdata2 = ['percentage defensive third', 'percentage neutral third', 'percentage offensive third']
        var1name = 'percentage defensive third'
        var2name = 'percentage neutral third'
        var3name = 'percentage offensive third'
        fig2 = go.Figure(data = [
        go.Bar(
            name = "Wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())]      
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())]
            )
        ])
        fig2.update_layout(barmode='group')
        graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)   

        xdata3 = ['percentage on ground', 'percentage low in air', 'percentage high in air']
        var1name = 'percentage on ground'
        var2name = 'percentage low in air'
        var3name = 'percentage high in air'
        fig3 = go.Figure(data = [
        go.Bar(
            name = "Wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())]      
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())]
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3)
    elif "sneakylastgame" in request.form:
        sneaky1 = allmatches_CK[0]
        sneaky1 = sneaky1[sneaky1['player name'] == 'Sneakyb4stard']
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']
        
        fig1 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())]      
        ),
        go.Bar(
            name = "Last game",
            x = xdata,
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky1[var1name].values), int(sneaky1[var2name].values), int(sneaky1[var3name].values)]
            )
        ])
        fig1.update_layout(barmode='group')
        graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)   

        xdata2 = ['percentage defensive third', 'percentage neutral third', 'percentage offensive third']
        var1name = 'percentage defensive third'
        var2name = 'percentage neutral third'
        var3name = 'percentage offensive third'
        fig2 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = xdata2,
            #y=[18, 15, 20]
            y=[int(sneaky['percentage defensive third'].mean()), int(sneaky['percentage neutral third'].mean()), int(sneaky['percentage offensive third'].mean())]
            
            
            
        ),
        go.Bar(
            name = "Last game",
            x = xdata2,
            #y=[18, 15, 20]
            y = [int(sneaky1[var1name].values), int(sneaky1[var2name].values), int(sneaky1[var3name].values)]
            )
        ])
        fig2.update_layout(barmode='group')
        graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)   

        xdata3 = ['percentage on ground', 'percentage low in air', 'percentage high in air']
        var1name = 'percentage on ground'
        var2name = 'percentage low in air'
        var3name = 'percentage high in air'
        fig3 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = xdata3,
            #y=[18, 15, 20]
            y=[int(sneaky['percentage on ground'].mean()), int(sneaky['percentage low in air'].mean()), int(sneaky['percentage high in air'].mean())]
            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,
            
            
        ),
        go.Bar(
            name = "Last game",
            x = xdata3,
            #y=[18, 15, 20]
            y = [int(sneaky1[var1name].values), int(sneaky1[var2name].values), int(sneaky1[var3name].values)]
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3)
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
        return render_template('index_C.html', plot1=graphJSON)

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
        
        return render_template('index_C.html', plot1=graphJSON)
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
            if(max(otherteamgoals['goals conceded'].values) > sneaky['goals conceded'].values):
                allmatches_CK_wins[countwins] = pd.concat(frames)
                countwins += 1
                #allmatches_CK_wins.append(pd.concat(frames), ignore_index = True)
            else:
                #allmatches_CK_wins.append(pd.concat(frames), ignore_index = True)
                allmatches_CK_losses[countlosses] = pd.concat(frames)
                countlosses += 1
        else:
            otherteamgoals = tempmatch[tempmatch['color'].str.contains('blue')]
            if(max(otherteamgoals['goals conceded'].values) > sneaky['goals conceded'].values):
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
    #sneakytotalscore = mean[allmatches_CK['player name'] == sn]
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
