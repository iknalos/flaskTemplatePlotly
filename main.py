import time
import csv

from flask import Flask
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 

import pymysql 
import json
import operator

app = Flask(__name__, static_url_path='')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
  
@app.route('/')
def home():
    return render_template('test.html', title='Home', msg='Welcome!')

@app.route('/csv')  
def download_csv():  
    csv = 'a,b,c\n1,2,3\n'  
    response = make_response(csv)
    cd = 'attachment; filename=mycsv.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response

    
if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
