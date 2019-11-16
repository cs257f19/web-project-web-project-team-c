#!/usr/bin/env python3

import flask
from flask import render_template, request
import json
import sys
from datasource import DataSource
import datetime

app = flask.Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    ds = DataSource('hayesrichn', 'orange227blue')
        
    today = ds.dateTimeToStr(datetime.datetime.today().date())
    today = ds.strToInt(today)
    # If the tables where constantly updated from yahooFiance. Because our tables are
    # not constantly updated. We will have place holder to have the most recent price
        
    today = 20191008
        
    returndata = ds.performDataQuery(['spy', 'btc', 'gld', 'irx'], 'adjcloseprice', today-1, today)
    print("initalReturnData", returndata)
    returndata = ds.formatData(returndata)
    listOfreturnHTML = makePriceChangeBetweenTwoDaysHTML(returndata)
    if request.method == 'GET':
        return render_template('index.html', listOfreturnHTML=listOfreturnHTML)
    if request.method == 'POST':
        dataset1 = request.form.get('dataset1')
        dataset2 = request.form.get('dataset2')
        datatype1 = request.form.get('datatype1')
        datatype2 = request.form.get('datatype2')
        regression(dataset1, dataset2, datatype1, datatype2, ds)


'''
Writes the html code to update the current prices and the color of the current price to
indicate positive or negative change in price
'''
def makePriceChangeBetweenTwoDaysHTML(returndata):
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
    firstDate = 20191007
    today = 20191008
    returndata1 = ds.performDataQuery([dataset1], datatype1, firstDate, today)
    returndata2 = ds.performDataQuery([dataset2], datatype2, firstDate, today)
    returndata = returndata1, returndata2
    print("returndata", returndata)
    #returndata = ds.formatData([returndata1, returndata2])
    #print("returndata", returndata)


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
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
