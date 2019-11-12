#!/usr/bin/env python3

import flask
from flask import render_template
import json
import sys
from datasource.py import DataSource

app = flask.Flask(__name__)

@app.route('/')

@app.route('/ourpage')
def index():
    data = DataSource.query.all()
    return render_template('index.html')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
