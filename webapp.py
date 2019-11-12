#!/usr/bin/env python3

import flask
from flask import render_template, request
import json
import sys
from datasource import DataSource

app = flask.Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['GET','POST'])
def result():
    if request.method == 'POST':
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        dataset1 = request.form.get('dataset1')
        dataset2 = request.form.get('dataset2')
        ds = DataSource('hayesrichn', 'orange227blue')
        ds.performDataQuery([dataset1, dataset2], 'openprice', date1, date2)
        return render_template('index.html')
    else:
        return render_template('index.html')
    return render_template('index.html')
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
