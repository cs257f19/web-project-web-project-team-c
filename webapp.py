#!/usr/bin/env python3

import flask
from flask import render_template, request
import json
import sys
from datasource import DataSource
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
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
    firstDate = 19600104
    today = 20191008
    returndata1 = ds.performDataQuery([dataset1], datatype1, firstDate, today)
    returndata2 = ds.performDataQuery([dataset2], datatype2, firstDate, today)
    returndata = ds.formatData([returndata1[1], returndata2[1]])
    
    if returndata == [[], []]:
        return (0, 0, [[], []])

    xValueList = []
    yValueList = []
    for tupleIndex in range(len(returndata)):
        if returndata[tupleIndex][1] != "No Data" and returndata[tupleIndex][2] != "No Data":
            yValueList.append(returndata[tupleIndex][1])
            xValueList.append([returndata[tupleIndex][2]])

    reg = LinearRegression().fit(xValueList, yValueList)
    plt.scatter(xValueList, yValueList,color='g')
    plt.figure()
    predicted_value = reg.predict(xValueList)
    plt.plot(xValueList, predicted_value,color='k')
    image = BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)
    print(returndata)
    return (base64.b64encode(image.read()), predicted_value, returndata)

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

        return render_template('results.html', returnhtml=returnhtml, returndata=returndata, dataset1=dataset1, dataset2=dataset2, datatype=datatype)
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

        returndata = regression(dataset1, dataset2, datatype1, datatype2, ds)
        returnhtml = "<h2>ANALYSIS RESULT</h2>"
        returnhtml = flask.Markup(returnhtml)

        return render_template('analysis.html', result=returndata[0].decode('utf8'), predicted_value=returndata[1], datatype1=datatype1, dataset1=dataset1, datatype2=datatype2, dataset2=dataset2, data=returndata[2], returnhtml=returnhtml)
    else:
        returnhtml = "<h2>Query Failed</h2>"
        returnhtml = flask.Markup(returnhtml)
        return render_template('results.html', returnhtml=returnhtml)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
