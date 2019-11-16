#!/usr/bin/env python3

import flask
from flask import render_template, request
import json
import sys
from datasource import DataSource

app = flask.Flask(__name__)

@app.route("/", methods['GET', 'POST'])
def index():
    if request.method == 'GET':
        ds = DataSource('hayesrichn', 'orange227blue')
        returndata = ds.performDataQuery(['irx', 'btc', 'spy', 'gld'], 'adjcloseprice', '20191007', '20191008')
        print(returndata)
        return render_template('index.html')

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
