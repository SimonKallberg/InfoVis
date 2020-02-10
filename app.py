import io
import random
import pandas as pd
import numpy as np
import json

from flask import Flask, render_template, Response
from flask import request
app = Flask(__name__)


#@app.route('/')
#def index():
    
from matplotlib import pyplot as plt
from math import pi

app = Flask(__name__)
df_csv = pd.read_csv('./matches_csv/testmatch2.csv', sep=';') # creating a sample dataframe
df_csv['assists']
df = pd.DataFrame({
'group': ['A', 'B', 'C', 'D', 'E', 'F'],
'Assists': df_csv['assists'],
'Shots': df_csv['shots'],
'Saves': df_csv['saves'],
'Goals': df_csv['goals'],
'Demos': df_csv['demos inflicted']
})

@app.route('/star')
def indexstar():
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
    plt.yticks([1,2,3], ["1","2","3"], color="grey", size=7)
    plt.ylim(0,4)


    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

    # Ind1
    values=df.loc[0].drop('group').values.flatten().tolist()    #make a list of all values
    values += values[:1]    #add first value at the end
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=df_csv['player name'].loc[0])
    ax.fill(angles, values, 'b', alpha=0.1)

    # Ind2
    values=df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=df_csv['player name'].loc[1])
    ax.fill(angles, values, 'r', alpha=0.1)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig('static/images/plot.png')
    return render_template('index.html', url='/static/images/plot.png')



@app.route('/C', methods=["GET", "POST"])
def indexC():
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
