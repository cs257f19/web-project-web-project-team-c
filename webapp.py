#!/usr/bin/env python3

import flask
from flask import render_template, request
import sys
from datasource import DataSource
import datetime
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score
from io import BytesIO
from matplotlib import pyplot as plt
import base64

app = flask.Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    ds = DataSource('hayesrichn', 'orange227blue')

    today = ds.dateTimeToStr(datetime.datetime.today().date())
    today = ds.strToInt(today)
    # If the tables were constantly updated from yahooFiance. Because our tables are
    # not constantly updated. We will have place holder to have the most recent price

    today = 20191008

    returndata = ds.performDataQuery(['spy', 'btc', 'gld', 'irx'], 'adjcloseprice', today-1, today)
    returndata = ds.formatData(returndata)
    listOfreturnHTML = makePriceChangeBetweenTwoDaysHTML(returndata)

    return render_template('index.html', listOfreturnHTML=listOfreturnHTML)

@app.route("/results.html", methods=['GET','POST'])
def result():
    if request.method == 'POST':
        ds = DataSource('hayesrichn', 'orange227blue')
        date1 = ds.strToInt(request.form.get('date1'))
        date2 = ds.strToInt(request.form.get('date2'))
        datatype = request.form.get('datatype')
        dataset1 = request.form.get('dataset1')
        dataset2 = request.form.get('dataset2')
        returndata = ds.performDataQuery([dataset1, dataset2], datatype, date1, date2)

        returnhtml = "<h2>DATA</h2>"
        returndata = ds.formatData(returndata)
        if returndata == []:
            returnhtml = "<h2>Query Failed</h2>"

        returnhtml = flask.Markup(returnhtml)

        dataset1ValueList = []
        dataset2ValueList = []
        datesValueList = []
        for tupleIndex in range(len(returndata)):
            if returndata[tupleIndex][1] != "No Data" and returndata[tupleIndex][2] != "No Data":
                dataset1ValueList.append(returndata[tupleIndex][1])
                dataset2ValueList.append(returndata[tupleIndex][2])
                datesValueList.append(returndata[tupleIndex][0])

        plt.figure()
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel('Dates')
        ax1.set_ylabel(str(dataset1) + " " + str(datatype), color=color)
        ax1.scatter(datesValueList, dataset1ValueList, color=color)

        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel(str(dataset2) + " " + str(datatype), color=color)  # we already handled the x-label with ax1
        ax2.scatter(datesValueList, dataset2ValueList, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        xticks= ax1.get_xticks()
        plt.xticks([xticks[0], xticks[-1]], visible=True, rotation="vertical")

        fig.tight_layout()

        image = BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)

        return render_template('results.html', returnhtml=returnhtml, returndata=reversed(returndata), dataset1=dataset1, dataset2=dataset2, datatype=datatype, image=base64.b64encode(image.read()).decode('utf8'))
    else:
        returnhtml = "<h2>Query Failed</h2>"
        returnhtml = flask.Markup(returnhtml)
        return render_template('results.html', returnhtml=returnhtml)

@app.route("/analysis.html", methods=['GET','POST'])
def analysisresults():
    if request.method == 'POST':
        ds = DataSource('hayesrichn', 'orange227blue')
        dataset1 = request.form.get('dataset1')
        datatype1 = request.form.get('datatype1')
        dataset2 = request.form.get('dataset2')
        datatype2 = request.form.get('datatype2')

        regression_data = regression(dataset1, dataset2, datatype1, datatype2, ds)
        returnhtml = "<h2>ANALYSIS RESULT</h2>"
        returnhtml = flask.Markup(returnhtml)

        return render_template('analysis.html', result=regression_data[0].decode('utf8'), predicted_value=regression_data[1], predictor_value=regression_data[2], datatype1=datatype1, dataset1=dataset1, datatype2=datatype2, dataset2=dataset2, returndata=reversed(regression_data[3]), returnhtml=returnhtml)
    else:
        returnhtml = "<h2>Query Failed</h2>"
        returnhtml = flask.Markup(returnhtml)
        return render_template('results.html', returnhtml=returnhtml)

def makePriceChangeBetweenTwoDaysHTML(returndata):
    '''
    Writes the html code to update the current prices and the color of the current
    price to indicate positive or negative change in price
    '''
    listOfreturnHTML = []
    for datasetIndex in range(1,len(returndata[0])):
        if returndata[1][datasetIndex] - returndata[0][datasetIndex] < 0:
            returnhtml = "<h4 style='color:red'> Current Price: " + str(returndata[1][datasetIndex]) + " ↓</h4>"
        else:
            returnhtml = "<h4 style='color:green'> Current Price: " + str(returndata[1][datasetIndex]) + " ↑</h4>"
        returnhtml = flask.Markup(returnhtml)
        listOfreturnHTML.append(returnhtml)
    return listOfreturnHTML

def regression(dataset1, dataset2, datatype1, datatype2, ds):
    '''
    Performs linear regression using dataset2 values as X values and dataset1 values as Y/target values.
    Returns: a tuple of the following format
     (Base64 encoded graph, predicted value if datatype of dataset 2 goes up 10 points, value of dataset2 going up 10 points, list containing all data used for regression)
    '''
    firstDate = 19600104
    today = 20191008
    returndata1 = ds.performDataQuery([dataset1], datatype1, firstDate, today)
    returndata2 = ds.performDataQuery([dataset2], datatype2, firstDate, today)
    returndata = ds.formatData([returndata1[0], returndata2[0]])

    if returndata == [[], []]:
        return (0, 0, 0, [[], []])

    xValueList = []
    yValueList = []
    for tupleIndex in range(len(returndata)):
        if returndata[tupleIndex][1] != "No Data" and returndata[tupleIndex][2] != "No Data":
            yValueList.append(returndata[tupleIndex][1])
            xValueList.append([returndata[tupleIndex][2]])

    reg = linear_model.LinearRegression().fit(xValueList, yValueList)
    plt.figure()
    plt.scatter(xValueList, yValueList, s=4, color='g')
    predicted_values = reg.predict(xValueList)
    plt.plot(xValueList, predicted_values, color='k')
    predicted_value = reg.predict([[xValueList[-1][0] + 10]])

    r2Text = r2_score(yValueList, predicted_values)
    plt.text(0.75, 0.75, "r^2: " + str(round(r2Text, 4)), style='italic', transform=plt.gca().transAxes, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 5})
    plt.xlabel(str(dataset2) + " " + str(datatype2))
    plt.ylabel(str(dataset1) + " " + str(datatype1))
    image = BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)

    return (base64.b64encode(image.read()), predicted_value[0], xValueList[-1][0] + 10, returndata)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()
    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
