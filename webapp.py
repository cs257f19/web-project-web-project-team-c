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
    if request.method == 'GET':
        ds = DataSource('hayesrichn', 'orange227blue')
        
        today = ds.dateTimeToStr(datetime.datetime.today().date())
        today = ds.strToInt(today)
        # If the tables where constantly updated from yahooFiance. Because our tables are
        # not constantly updated. We will have place holder to have the most recent price
        
        today = 20191008
        
        returndata = ds.performDataQuery(['spy', 'btc', 'gld', 'irx'], 'adjcloseprice', today-1, today)
        returndata = ds.formatData(returndata)
        print("Today:", today)
        print("returndata:", returndata)
        listOfreturnHTML = makePriceChangeBetweenTwoDaysHTML(returndata)
        return render_template('index.html', listOfreturnHTML=listOfreturnHTML)
        
def makePriceChangeBetweenTwoDaysHTML(returndata):
    listOfreturnHTML = []
    for datasetIndex in range(1,len(returndata[0])):
        if returndata[1][datasetIndex] - returndata[0][datasetIndex] < 0:
            returnhtml = "<h4 style='color:red'>", returndata[1][datasetIndex], " ↓</h4>"
        else:
            returnhtml = "<h4 style='color:green'>", returndata[1][datasetIndex], " ↑</h4>"
        
        print("returndata", returndata[1][datasetIndex])
        print("returnhtml", returnhtml)
        returnhtml = flask.Markup(returnhtml)
        listOfreturnHTML.append(returnhtml)
    return listOfreturnHTML


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
