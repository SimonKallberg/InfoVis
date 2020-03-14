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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import pi
import seaborn as sns
import sklearn as sklearn

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
    return render_template('index_starplot.html', url='/static/images/plotsolo.png')

@app.route('/starplot', methods=["GET","POST"])
def update_star_plot():
    if request.method == 'POST':
        read_data()
        variables_for_star()
        #create_star_plot()
        #create_star_plot('shots', 'shooting percentage', 'bpm', "percentage supersonic speed", "avg speed")
        return redirect(url_for('update_star_plot'))
    return render_template('index_starplot.html', url='/static/images/plotsolo.png')

@app.route('/starplot_own', methods=["GET","POST"])
def own_star_plots():
    if request.method == 'POST':
        read_data()
        #variables_for_star()
        #create_star_plot()
        create_star_plot('shots', 'shooting percentage', 'bpm', "percentage supersonic speed", "avg speed", "def")
        create_star_plot('saves', 'score', 'percentage defensive third', "percentage behind ball", "assists", "def2")
        return redirect(url_for('own_star_plots'))
    return render_template('index_starplot_own.html', url='/static/images/plotdef.png', url2='/static/images/plotdef2.png')



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
@app.route('/procomparison', methods=["GET", "POST"])
def comparisonpage():
    read_data()
    return create_procomparison()
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
            y = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            text = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Kuzon",
            x = xdata,
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            text = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            textposition = 'auto'
            )
        ])

        #fig1.layout.yaxis.tickformat = '%'
        fig1.update_layout(barmode='group')
        graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        xdata2 = ['percentage defensive third', 'percentage neutral third', 'percentage offensive third']
        fig2 = go.Figure(data = [
        go.Bar(
            name = "sneaky",
            x = xdata2,
            #y=[18, 15, 20]
            y=[int(sneaky['percentage defensive third'].mean()), int(sneaky['percentage neutral third'].mean()), int(sneaky['percentage offensive third'].mean())],
            text = [int(sneaky['percentage defensive third'].mean()), int(sneaky['percentage neutral third'].mean()), int(sneaky['percentage offensive third'].mean())],
            textposition = 'auto'
            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,


        ),
        go.Bar(
            name = "kuzon",
            x = xdata2,
            #y=[18, 15, 20]
            y = [int(kuzon['percentage defensive third'].mean()), int(kuzon['percentage neutral third'].mean()), int(kuzon['percentage offensive third'].mean())],
            text = [int(kuzon['percentage defensive third'].mean()), int(kuzon['percentage neutral third'].mean()), int(kuzon['percentage offensive third'].mean())],
            textposition = 'auto'
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
            y=[int(sneaky['percentage on ground'].mean()), int(sneaky['percentage low in air'].mean()), int(sneaky['percentage high in air'].mean())],
            text = [int(sneaky['percentage on ground'].mean()), int(sneaky['percentage low in air'].mean()), int(sneaky['percentage high in air'].mean())],
            textposition = 'auto'
            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,


        ),
        go.Bar(
            name = "kuzon",
            x = xdata3,
            #y=[18, 15, 20]
            y = [int(kuzon['percentage on ground'].mean()), int(kuzon['percentage low in air'].mean()), int(kuzon['percentage high in air'].mean())],
            text = [int(kuzon['percentage on ground'].mean()), int(kuzon['percentage low in air'].mean()), int(kuzon['percentage high in air'].mean())],
            textposition = 'auto'
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3, data="The graphs below represent average stats comparison between sneakybastard and Kuzon.")
        #return graphJSON
    elif "sneakywinsandlosses" in request.form:
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            text = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            text = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            textposition = 'auto'
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
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            text = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            text = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            textposition = 'auto'
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
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            text = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            text = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            textposition = 'auto'
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3, data="This is a comparison of stats when Sneaky win and lose")
    elif "kuzonwinsandlosses" in request.form:
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            text = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            textposition = 'auto'

        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            text = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            textposition = 'auto'

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
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            text = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            textposition = 'auto'

        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            text = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            textposition = 'auto'
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
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            text = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Losses",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            text = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            textposition = 'auto'
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3, data="This is a comparison of stats when Kuzons win and lose")
    elif "sneakylastgame" in request.form:
        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            text = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Last game",
            x = xdata,
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            text = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            textposition = 'auto'
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
            y=[int(sneaky['percentage defensive third'].mean()), int(sneaky['percentage neutral third'].mean()), int(sneaky['percentage offensive third'].mean())],
            text = [int(sneaky['percentage defensive third'].mean()), int(sneaky['percentage neutral third'].mean()), int(sneaky['percentage offensive third'].mean())],
            textposition = 'auto'


        ),
        go.Bar(
            name = "Last game",
            x = xdata2,
            #y=[18, 15, 20]
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            text = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            textposition = 'auto'
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
            y=[int(sneaky['percentage on ground'].mean()), int(sneaky['percentage low in air'].mean()), int(sneaky['percentage high in air'].mean())],
            text = [int(sneaky['percentage on ground'].mean()), int(sneaky['percentage low in air'].mean()), int(sneaky['percentage high in air'].mean())],
            textposition = 'auto'

            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,


        ),
        go.Bar(
            name = "Last game",
            x = xdata3,
            #y=[18, 15, 20]
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            text = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            textposition = 'auto'
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3, data="This is a comparison of stats for sneakys last game and average stats")
    elif "kuzonlastgame" in request.form:

        xdata = ['percentage supersonic speed', 'percentage boost speed', 'percentage slow speed']

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            text = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Last game",
            x = xdata,
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            text = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            textposition = 'auto'

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
            y=[int(kuzon['percentage defensive third'].mean()), int(kuzon['percentage neutral third'].mean()), int(kuzon['percentage offensive third'].mean())],
            text = [int(kuzon['percentage defensive third'].mean()), int(kuzon['percentage neutral third'].mean()), int(kuzon['percentage offensive third'].mean())],
            textposition = 'auto'


        ),
        go.Bar(
            name = "Last game",
            x = xdata2,
            #y=[18, 15, 20]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            text = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            textposition = 'auto'

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
            y=[int(kuzon['percentage on ground'].mean()), int(kuzon['percentage low in air'].mean()), int(kuzon['percentage high in air'].mean())],
            text = [int(kuzon['percentage on ground'].mean()), int(kuzon['percentage low in air'].mean()), int(kuzon['percentage high in air'].mean())],
            textposition = 'auto'

            #y = [int(sneaky['percentage supersonic speed'].values), 15, 20]
            #x=allmatches_CK_wins[0]['player name', 'percentage boost speed'], # assign x as the dataframe column 'x'
            #x = xdata,


        ),
        go.Bar(
            name = "Last game",
            x = xdata3,
            #y=[18, 15, 20]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            text = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            textposition = 'auto'
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3, data="This is a comparison of stats for kuzons last game and average stats")
    elif "EverystatKuzon" in request.form:

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            text =  [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Last game",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            text = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Kuzon wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            text = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            textposition = 'auto'

        ),
        go.Bar(
            name = "Kuzon lost",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            text = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            textposition = 'auto'


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
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            text = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Last game",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            text = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            textposition = 'auto'

        ),
        go.Bar(
            name = "Kuzon wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            text = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            textposition = 'auto'

        ),
        go.Bar(
            name = "Kuzon lost",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            text = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            textposition = 'auto'

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
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            text=[int(kuzon[var1name].mean()), int(kuzon[var2name].mean()), int(kuzon[var3name].mean())],
            textposition='auto'
        ),
        go.Bar(
            name = "Last game",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            text = [int(kuzonlast[var1name].values), int(kuzonlast[var2name].values), int(kuzonlast[var3name].values)],
            textposition='auto'
        ),
        go.Bar(
            name = "Kuzon wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            text = [int(kuzon1[var1name].mean()), int(kuzon1[var2name].mean()), int(kuzon1[var3name].mean())],
            textposition='auto'
        ),
        go.Bar(
            name = "Kuzon lost",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            text = [int(kuzon2[var1name].mean()), int(kuzon2[var2name].mean()), int(kuzon2[var3name].mean())],
            textposition='auto'
            )
        ])
        fig3.update_layout(barmode='group')
        #fig3.update_layout(barmode='stack')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)





        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3, data= "this is a graph with kuzons last game, average stats aswell as wins and losses")
    elif "EverystatSneaky" in request.form:

        fig1 = go.Figure(data = [
        go.Bar(
            name = "Average stats",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            text = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            textposition = 'auto'

        ),
        go.Bar(
            name = "Last game",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            text = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            textposition = 'auto'

        ),
        go.Bar(
            name = "sneaky wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            text = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            textposition = 'auto'

        ),
        go.Bar(
            name = "sneaky lost",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            text = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            textposition = 'auto'
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
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            text = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "Last game",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            text = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            textposition = 'auto'
        ),
        go.Bar(
            name = "sneaky wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            text = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "sneaky lost",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            text = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            textposition = 'auto'
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
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y=[int(sneaky['percentage supersonic speed'].values), int(sneaky['percentage boost speed'].values), int(sneaky['percentage slow speed'].values)]
            y = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            text = [int(sneaky[var1name].mean()), int(sneaky[var2name].mean()), int(sneaky[var3name].mean())],
            textposition = 'auto'

        ),
        go.Bar(
            name = "Last game",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            text = [int(sneakylast[var1name].values), int(sneakylast[var2name].values), int(sneakylast[var3name].values)],
            textposition = 'auto'

        ),
        go.Bar(
            name = "sneaky wins",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            text = [int(sneaky1[var1name].mean()), int(sneaky1[var2name].mean()), int(sneaky1[var3name].mean())],
            textposition = 'auto'
        ),
        go.Bar(
            name = "sneaky lost",
            x = [var1name, var2name, var3name],
            #y=[18, 15, 20]
            #y = [int(kuzon['percentage supersonic speed'].values), int(kuzon['percentage boost speed'].values), int(kuzon['percentage slow speed'].values)]
            y = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            text = [int(sneaky2[var1name].mean()), int(sneaky2[var2name].mean()), int(sneaky2[var3name].mean())],
            textposition = 'auto'
            )
        ])
        fig3.update_layout(barmode='group')
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)





        return render_template('index_C.html', plot1=graphJSON, plot2=graphJSON2, plot3=graphJSON3, data= "this is a graph with sneakys last game, average stats aswell as wins and losses")
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

def variables_for_star():
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
    create_star_plot(var1, var2, var3, var4, var5, "solo")

def create_procomparison():
    average_chausette = pd.read_csv('./matches_csv/Chausette45.csv', sep=';')
    print("first avg" + '\n' + str(average_chausette), file=sys.stderr)
    average_chausette = average_chausette.mean()  #have same index value
    print("AVERAGE DF" + '\n'+ str(average_chausette), file=sys.stderr)

    average_df = pd.read_csv('./matches_csv/average.csv', sep=';')
    average_df = average_df.mean()  #have same index value


    average_sypical = pd.read_csv('./matches_csv/Sypical.csv', sep=';')
    average_sypical = average_sypical.mean()  #have same index value

    mainDF = pd.concat(allmatches_CK)
    kuzonDF = mainDF[mainDF['player name'] == 'Kuzon']
    sneakyDF = mainDF[mainDF['player name'] == 'Sneakyb4stard']
    kuzonDF_mean = kuzonDF.mean()
    sneakyDF_mean = sneakyDF.mean()
    newDF = [kuzonDF_mean, average_sypical, average_df, average_chausette, sneakyDF_mean]

    df_csv_new = pd.concat(newDF, axis=1)
    df_csv_new = df_csv_new.T
    df_csv_new = df_csv_new.reset_index()
    df_csv_test = df_csv_new
    df_csv_test = df_csv_test[df_csv_test != 1]
    df_csv_test = df_csv_test.dropna(axis='columns')
    print('NYA' + '\n' +  str(df_csv_test), file=sys.stderr)
    #df_csv_test = df_csv_test.apply(pd.to_numeric, errors='coerce')
    #df_csv_test = df_csv_test.dropna(axis='columns')
    #df_csv_test = df_csv_test.reset_index()
    #df_csv_test.loc[3] = df_csv_test.iloc[0] / df_csv_test.iloc[2]
    #df_csv_test.loc[4] = df_csv_test.iloc[1] / df_csv_test.iloc[2]
    #print('TEST: ' +  str(df_csv_test['score']), file=sys.stderr)

    #testsneaky = [sneakyDF_mean, kuzonDF_mean]
    #testkuzon = [kuzonDF_mean, average_chausette]
    #testsneaky = pd.concat(testsneaky1, axis=1)
    #testsneaky = testsneaky.T
    #testsneaky = testsneaky.reset_index()
    #df_csv_test = testsneaky
    #df_csv_test = df_csv_test[df_csv_test != 1]
    #df_csv_test = df_csv_test.dropna(axis='columns')
    df_csv_pca = df_csv_test
    df_csv_test = abs(df_csv_test.pct_change(axis='columns'))
    df_csv_test = df_csv_test[df_csv_test < 1]
    df_csv_test = df_csv_test.dropna(axis='columns')

    #df_csv_test = df_csv_test.mean(numeric_only=True)
    #sneakycomp = testsneaky
    #sneakycomp = pd.concat(testsneaky, axis=1)
    #sneakycomp = sneakycomp.T
    #sneakycomp = sneakycomp.reset_index()

    print('newtestcomp: ' + str(df_csv_test), file=sys.stderr)
    print('newtestcomp1: ' + str(df_csv_test.iloc[1,:].mean()), file=sys.stderr)
    print('newtestcomp2: ' + str(df_csv_test.iloc[2,:].mean()), file=sys.stderr)
    print('newtestcomp3: ' + str(df_csv_test.iloc[3,:].mean()), file=sys.stderr)
    print('newtestcomp4: ' + str(df_csv_test.iloc[4,:].mean()), file=sys.stderr)


    #sneakycomp = sneakycomp.apply(lambda x: x/x.sum(), axis=1)

    #sneakycomp = sneakycomp.dropna()
    #print('testcomp: ' + str(abs(sneakycomp.pct_change())), file=sys.stderr)

    #sneakycomparechausette = abs(sneakycomp.pct_change())
    #sneakycomparechausette = sneakycomparechausette.apply(pd.to_numeric, errors='coerce')
    #sneakycomparechausette = sneakycomparechausette.dropna(axis='columns')

    #print('check for 1s :' + str(sneakycomparechausette['shots conceded']), file=sys.stderr)
    #sneakycomparechausette = sneakycomparechausette[sneakycomparechausette != 1]
    #sneakycomparechausette = sneakycomparechausette.astype('float')
    #sneakycomparechausette = sneakycomparechausette.dropna()
    #sneaky_finalmatch = sneakycomparechausette.mean()
    #sneaky_finalmatch
    #print('testmatch: ' + str(sneaky_finalmatch) + 'shape' + str(sneaky_finalmatch.head()), file=sys.stderr)
    returnstring = "percentage difference(mean) between kuzon and Sypical is: " + str(df_csv_test.iloc[3,:].mean()) #+ "<br>" + "hej"
    returnstring2 = "percentage difference(mean) between Sneaky and Sypical is: " + str(df_csv_test.iloc[4,:].mean()) #+ "<br>" + "hej"
    returnstring3 = "percentage difference(median) between kuzon and Sypical is: " + str(df_csv_test.iloc[3,:].median()) #+ "<br>" + "hej"
    returnstring4 = "percentage difference(median) between Sneaky and Sypical is: " + str(df_csv_test.iloc[4,:].median()) #+ "<br>" + "hej"
    returnstring5 = "percentage difference(variance) between kuzon and Sypical is: " + str(df_csv_test.iloc[3,:].var()) #+ "<br>" + "hej"
    returnstring6 = "percentage difference(variance) between Sneaky and Sypical is: " + str(df_csv_test.iloc[4,:].var()) #+ "<br>" + "hej"

    #plotting mean and variance
    mean = np.array([df_csv_test.iloc[1,:].mean(), df_csv_test.iloc[2,:].mean(), df_csv_test.iloc[3,:].mean(), df_csv_test.iloc[4,:].mean()])
    median = np.array([df_csv_test.iloc[1,:].median(), df_csv_test.iloc[2,:].median(), df_csv_test.iloc[3,:].median(), df_csv_test.iloc[4,:].median()])
    var = np.array([df_csv_test.iloc[1,:].var(), df_csv_test.iloc[2,:].var(), df_csv_test.iloc[3,:].var(), df_csv_test.iloc[4,:].var()])

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt

    #fig2 = plt.figure(figsize = (8,8))
    #ax = fig2.add_subplot(1,1,1)
    #ax.set_xlabel('mean value', fontsize = 15)
    #ax.set_ylabel('median value', fontsize = 15)
    #ax.set_title('variance', fontsize = 20)
    x = ['Sypical', 'Average player', 'Chausette45', 'Sneaky']
    fig, (ax1, ax2) = plt.subplots(nrows=2)

    ax1.errorbar(x, mean, yerr=var, fmt='o', capsize=4)
    ax1.set_title('Mean percentage difference from kuzon, with variance included')

    ax2.errorbar(x, median, yerr=var, fmt='o', capsize=4)
    ax2.set_title('Median percentage difference from kuzon, with variance included')
    fig.tight_layout(pad=3.0)
    #plt.errorbar(x, y, e, linestyle='None', marker='^', capsize=3)
    #plt.set_title('plot of percentage differences with mean, median and variance shown')
    #plt.set_xlabel('Mean values')
    #plt.set_ylabel('Median values')

    plt.savefig("static/images/plot" + "pro" + ".png")
    #plt.savefig("static/images/plot" + str(name) + ".png")
    plt.clf()

    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    #x = df_csv_new.loc[:,:].str.contains('score').drop()
    x = df_csv_pca.iloc[:, 2:].values
    y = df_csv_pca.iloc[:, 1].values
    #y = df_csv_pca[['goals']]
    print('PCAtest: ' + str(df_csv_pca), file=sys.stderr)

    ## Test for PCA -> plot


    x = StandardScaler().fit_transform(x)


    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDF = pd.DataFrame(data = principalComponents, columns = ['pc1', 'pc2'])
    targets = ['Kuzon', 'Sypical', 'Average player', 'Chausette45', 'Sneakybastard']
    newddF = pd.DataFrame(targets, columns = ['player'])
    finalDF = pd.concat([principalDF, newddF], axis=1)

    print('newtestcomp4: ' + str(finalDF), file=sys.stderr)

    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1)
    #xs = range(100)
    #ys = [random.randint(1,50) for x in xs]

    #colors = ['r']
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('PCA over average stats for n=5 players', fontsize = 20)
    targets = ['Kuzon', 'Sypical', 'Average player', 'Chausette45', 'Sneakybastard']
    colors = ['r', 'g', 'b', 'c', 'k']
    counter = 0
    #for target, color in zip(targets, colors):
        #indicesToKeep = finalDF.iloc[:,1] == target

#funkar med detta som är utkommenterat som en string men fick det att funka med en for-loop ist.
    """
    ax.scatter(finalDF.loc[0, 'pc1']
    , finalDF.loc[0, 'pc2'],
    label=targets[0],
    c = colors[0],
    s = 100
    )
    ax.scatter(finalDF.loc[1, 'pc1']
    , finalDF.loc[1, 'pc2'],
    label=targets[1],
    c = colors[1],
    s = 100
    )
    ax.scatter(finalDF.loc[2, 'pc1']
    , finalDF.loc[2, 'pc2'],
    label=targets[2],
    c = colors[2],
    s = 100
    )
    ax.scatter(finalDF.loc[3, 'pc1']
    , finalDF.loc[3, 'pc2'],
    label=targets[3],
    c = colors[3],
    s = 100
    )
    ax.scatter(finalDF.loc[4, 'pc1']
    , finalDF.loc[4, 'pc2'],
    label=targets[4],
    c = colors[4],
    s = 100
    )
    ax.legend()
        #counter += 1
    #ax.legend()
    #import matplotlib.patches as mpatches

    #colorhandler = mpatches.Patch(color=colors, label=targets)
    #ax.legend(handles=colorhandler)
    #ax.legend.key
    ax.grid()
    #ax.plot(xs,ys)
"""

    for target, color in zip(targets,colors):
        indicesToKeep = finalDF['player'] == target
        ax.scatter(finalDF.loc[indicesToKeep, 'pc1']
               , finalDF.loc[indicesToKeep, 'pc2']
              , c = color
               , s = 100)

    ax.legend(targets)
    ax.grid()
    fig.savefig("static/images/plot" + "pro2" + ".png")
    #plt.savefig("static/images/plot" + str(name) + ".png")
    fig.clf()
    from flask import Response
    #import io
    #output = io.BytesIO()
    #FigureCanvas(fig).print_png(output)
    #return Response(output.getvalue(), mimetype='image/png')
    #return render_template('propage.html', data=returnstring, data2=returnstring2, data3=returnstring3, data4=returnstring4, data5=returnstring5, data6=returnstring6,  url='/static/images/plotpro.png')
    return render_template('propage.html', url='/static/images/plotpro.png', url2='/static/images/plotpro2.png')

def create_star_plot(var1, var2, var3,var4,var5, name):
    df_csv = pd.read_csv('./matches_csv/testmatch0.csv', sep=';') # creating a sample dataframe0
    mainDF = pd.concat(allmatches_CK)
    kuzonDF = mainDF[mainDF['player name'] == 'Kuzon']
    sneakyDF = mainDF[mainDF['player name'] == 'Sneakyb4stard']
    kuzonDF_mean = kuzonDF.mean()
    sneakyDF_mean = sneakyDF.mean()

    average_df = pd.read_csv('./matches_csv/average.csv', sep=';')
    print("first avg" + '\n' + str(average_df), file=sys.stderr)
    average_df = average_df.mean()  #have same index value
    print("AVERAGE DF" + '\n'+ str(average_df), file=sys.stderr)
    newDF = [kuzonDF_mean, sneakyDF_mean, average_df]
    df_csv_new = pd.concat(newDF, axis=1)
    df_csv_new = df_csv_new.T
    df_csv_new = df_csv_new.reset_index()
    df_csv_test = df_csv_new
    print('NYA' + '\n' +  str(df_csv_new), file=sys.stderr)
    df_csv_test = df_csv_test.apply(pd.to_numeric, errors='coerce')
    df_csv_test = df_csv_test.dropna(axis='columns')
    #df_csv_test = df_csv_test.reset_index()
    df_csv_test.loc[3] = df_csv_test.iloc[0] / df_csv_test.iloc[2]
    df_csv_test.loc[4] = df_csv_test.iloc[1] / df_csv_test.iloc[2]
    print('TEST: ' +  str(df_csv_test), file=sys.stderr)

    df = pd.DataFrame({
    'group': ['A', 'B', 'C', 'D', 'E'],
    "1. " + var1: df_csv_test[var1],
    "2. " + var2: df_csv_test[var2],
    "3. " + var3: df_csv_test[var3],
    "4. " + var4: df_csv_test[var4],
    "5. " + var5: df_csv_test[var5]
    })

    #Base taken from https://python-graph-gallery.com/391-radar-chart-with-several-individuals/
    #Since matplotlib didnt have one implemented
    #have made several changes for our project
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

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0.5,1,2,3], ["0.5","1","2","3"], color="grey", size=7)
    plt.ylim(0,3)


    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

    # Ind1
    values=df.loc[3].drop('group').values.flatten().tolist()    #make a list of all values
    values += values[:1]    #add first value at the end
    ax.plot(angles, values, linewidth=1, linestyle='solid', label='Kuzon')
    ax.fill(angles, values, 'b', alpha=0.1)

    # Ind2
    values=df.loc[4].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label='Sneakybastard')
    ax.fill(angles, values, 'r', alpha=0.1)

    # Ind3
    values = [1.0, 1.0, 1.0,1.0,1.0,1.0]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label='Average player')
    ax.fill(angles, values, 'r', alpha=0.1)

    # Add legend
    plt.legend(loc='lower right', bbox_to_anchor=(1.0, 0.8))
    plt.savefig("static/images/plot" + str(name) + ".png")
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
