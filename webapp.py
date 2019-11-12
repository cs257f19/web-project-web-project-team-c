#!/usr/bin/env python3

import flask
from flask import render_template
import json
import sys
#from datasource import DataSource

app = flask.Flask(__name__)

#@app.route("/", methods=['GET','POST'])
@app.route('/')
def result():
   # if request.method == 'POST':
    #    date1 = request.form('date1')
     #   date2 = request.form('date2')
      #  dataset1 = request.form('dataset1')
       # dataset2 = request.form('dataset2')
       # return render_template('index.html')
   # else:
    #    return render_template('index.html')
    return render_template('index.html')
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
