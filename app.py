from __future__ import print_function # In python 2.7
import sys
import io
import random
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go
import logging
import sys
import os
from flask import Flask, render_template, Response, redirect, url_for
from flask import request
from matplotlib import pyplot as plt
from math import pi
import math


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

numberofmatches = 20
allmatches = {}
allmatches_CK = {}
allmatches_CK_wins = {}
allmatches_CK_losses = {}
kuzon = {}
sneaky = {}

@app.route('/starplot')
def indexstar():
    return render_template('index_starplot.html', url='/static/images/plot.png')

@app.route('/starplot', methods=["GET","POST"])
def update_star_plot():
    if request.method == 'POST':
        read_data()
        create_star_plot()
        return redirect(url_for('update_star_plot'))

    return render_template('index_starplot.html', url='/static/images/plot.png')


@app.route('/C', methods=["GET", "POST"])
def indexC():
    #bar = create_plot()
    return create_plot()
    #return render_template('index.html', plot=bar)

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html', url='/static/images/plot.png')

@app.route('/content', methods=["GET", "POST"])
def content():
    return render_template('content.html', url='/static/images/plot.png')

@app.route('/kuzon', methods=["GET", "POST"])
def home_page():
    return render_template('index_homepage.html')

@app.route('/index', methods=["GET", "POST"])
def index_page():
    return render_template('index_homepage.html')

@app.route('/barcharts', methods=["GET", "POST"])
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
    kuzon1 = df_win[df_win['player name'] == 'Kuzon']

    df_lose = pd.concat(allmatches_CK_losses)
    sneaky2 = df_lose[df_lose['player name'] == 'Sneakyb4stard']
    kuzon2 = df_lose[df_lose['player name'] == 'Kuzon']
    #sneaky1 = pd.concat(allmatches_CK_wins['player name'].str.contains('Sneakyb4stard'))
    #sneaky2 = pd.concat(allmatches_CK_losses['player name'].str.contains('Sneakyb4stard'))
    
    df = pd.concat(allmatches_CK)
    #print('testmean' + str(sneaky1['score'].mean()), file=sys.stderr)
    print('sneaky1' + str(sneaky2['goals']), file=sys.stderr)
    #for i in range(0, numberofmatches):
        #print('testoutput' + str(allmatches_CK_wins[i]), file=sys.stderr)
    
    sneaky = df[df['player name'] == 'Sneakyb4stard']
    kuzon = df[df['player name'] == 'Kuzon']

    sneakylast = allmatches_CK[0]
    sneakylast = sneakylast[sneakylast['player name'] == 'Sneakyb4stard']
    kuzonlast = allmatches_CK[0]
    kuzonlast = kuzonlast[kuzonlast['player name'] == 'Kuzon']
    
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
    elif "sneakywinsandlosses" in request.form:
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
    elif "kuzonwinsandlosses" in request.form:
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())]      
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())]
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
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())]      
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())]
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
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())]      
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())]
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3)    
    elif "sneakylastgame" in request.form:
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
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)]
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
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)]
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
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)]
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3)
    elif "kuzonlastgame" in request.form:
        
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']
        
        fig1 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())]      
        ),
        go.Bar(
            name = "Last game",
            x = xdata,
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)]
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
            y=[int(kuzon['percentage defensive third'].mean()), int(kuzon['percentage neutral third'].mean()), int(kuzon['percentage offensive third'].mean())]
            
            
            
        ),
        go.Bar(
            name = "Last game",
            x = xdata2,
            #y=[18, 15, 20]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)]
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
            y=[int(kuzon['percentage on ground'].mean()), int(kuzon['percentage low in air'].mean()), int(kuzon['percentage high in air'].mean())]
            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,
            
            
        ),
        go.Bar(
            name = "Last game",
            x = xdata3,
            #y=[18, 15, 20]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)]
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)   
        
        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3)
    elif "showmeall" in request.form:

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())]      
        ),
        go.Bar(
            name = "Last game",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)]
        ),
        go.Bar(
            name = "Kuzon wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())]
        ),
        go.Bar(
            name = "Kuzon lost",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())]
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
            y=[int(kuzon['percentage defensive third'].mean()), int(kuzon['percentage neutral third'].mean()), int(kuzon['percentage offensive third'].mean())]
            
            
            
        ),
        go.Bar(
            name = "Last game",
            x = xdata2,
            #y=[18, 15, 20]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)]
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
            y=[int(kuzon['percentage on ground'].mean()), int(kuzon['percentage low in air'].mean()), int(kuzon['percentage high in air'].mean())]
            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,
            
            
        ),
        go.Bar(
            name = "Last game",
            x = xdata3,
            #y=[18, 15, 20]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)]
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder) 





        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3)
    else:
        return render_template('bar_default.html')

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

        return render_template('index_C.html', plot=graphJSON)
        #return graphJSON
    elif "match2" in request.form:
        data = [
        go.Bar(
            x=allmatches[1]['player name'], # assign x as the dataframe column 'x'
            y=allmatches[1]['score']
        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('index_C.html', plot=graphJSON)
        #return graphJSON
    else:
        data = [
        go.Bar(
            x=allmatches[0]['player name'], # assign x as the dataframe column 'x'
            y=allmatches[0]['score']
        )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('index_C.html', plot=graphJSON)
        #return graphJSON

    #graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    #return graphJSON

def create_star_plot():
    var1 = request.form.get('Offensive')
    if var1 is None:
        var1 = 'shots'
    var2 = request.form.get('Defensive')
    if var2 is None:
        var2 = 'saves'
    var3 = request.form.get('Positioning')
    if var3 is None:
        var3 = 'percentage defensive third'
    var4 = request.form.get('Misc')
    if var4 is None:
        var4 = 'demos inflicted'

    var5 = request.form.get('Speed')
    if var5 is None:
        var5 = 'percentage supersonic speed'

    df_csv = pd.read_csv('./matches_csv/testmatch0.csv', sep=';') # creating a sample dataframe0
    kuzonAvgVar1 = 0
    mainDF = pd.concat(allmatches_CK)
    kuzonDF = mainDF[mainDF['player name'] == 'Kuzon']
    sneakyDF = mainDF[mainDF['player name'] == 'Sneakyb4stard']
    kuzonDF_mean = kuzonDF.mean()
    sneakyDF_mean = sneakyDF.mean()

    #print(kuzonDF_mean, file=sys.stderr)
    newDF = [kuzonDF_mean, sneakyDF_mean]
    print('kuzmeans' + '\n' + str(kuzonDF_mean), file=sys.stderr)
    print('snakmeans' + '\n' + str(sneakyDF_mean), file=sys.stderr)
    print('NEWDF' + '\n' + str(newDF), file=sys.stderr)


    df_kuzon = df_csv[df_csv['player name'].str.contains('Kuzon')]
    df_sneaky = df_csv[df_csv['player name'].str.contains('Sneakyb4stard')]
    frames = [df_kuzon, df_sneaky]
    print('dfkuz' + '\n' + str(df_kuzon), file=sys.stderr)
    df_csv_new = pd.concat(newDF, axis=1)
    df_csv_new = df_csv_new.T
    #df_csv_new2 = df_csv_new2.reset_index()
    print('NYA' + '\n' +  str(df_csv_new), file=sys.stderr)

    if var5 == 'avg speed':
        df_csv_new[var5] = df_csv_new[var5]/250
    if var5 == 'percentage supersonic speed':
        df_csv_new[var5] = df_csv_new[var5]/2
    if var2 == "goals conceded while last defender":
        var2name = "Last def. when conceded"
    else:
        var2name = var2

    df = pd.DataFrame({
    'group': ['A', 'B'],
    var1: df_csv_new[var1],
    var2name: df_csv_new[var2],
    var3: df_csv_new[var3]/10,
    var4: df_csv_new[var4],
    var5: df_csv_new[var5]
    })
    #TAKEN FROM https://python-graph-gallery.com/391-radar-chart-with-several-individuals/
    #Since matplotlib didnt have one implemented
    # ------- PART 1: Create background
    # number of variable

    categories=list(df)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)

    yTickValues = df.max()
    maxValue = yTickValues.drop(['group'])
    maxValue = maxValue.max()

    maxValue = math.ceil(maxValue / 2.) * 2
    print(maxValue, file=sys.stderr)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([1,maxValue/4,maxValue/2,3*maxValue/4,maxValue], ["1",maxValue/4,maxValue/2,3*maxValue/4,maxValue], color="grey", size=7)
    plt.ylim(0,maxValue)


    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

    # Ind1
    values=df.loc[0].drop('group').values.flatten().tolist()    #make a list of all values
    values += values[:1]    #add first value at the end
    ax.plot(angles, values, linewidth=1, linestyle='solid', label='Kuzon')
    ax.fill(angles, values, 'b', alpha=0.1)

    # Ind2
    values=df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label='Sneaky')
    ax.fill(angles, values, 'r', alpha=0.1)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.01, 0.01))
    plt.savefig('static/images/plot.png')
    plt.clf()

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
