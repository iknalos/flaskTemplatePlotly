import time
import csv

from flask import Flask
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response, render_template

import pymysql 
import json
import operator

app = Flask(__name__, static_url_path='')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def home():
    #return '<b>hi</b>'
    return render_template('test.html', title='Home', msg='CasesPlot Should be executed to see results')
	
@app.route('/CancerCasesPlot',methods = ['GET','POST'])
def CancerCasesPlot():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    qyear = request.args.get('year')
    if qyear is not None:
        sql = 'SELECT * FROM `rahul_Solanki` WHERE YEAR(`Date`) = %s ORDER BY `Date`';
        cur.execute(sql,(qyear))
    else:
        sql = 'SELECT * FROM `rahul_Solanki` ORDER BY `Date`';
        cur.execute(sql)
    jsx = []
    jsy = []
    
    for row in cur:
        jsx.append(row['Date'])
        jsy.append(row['Cases'])
    jsdata = {'x':jsx,'y':jsy}
    return render_template('CasesPlot.html', title='Cases Plot', data=jsdata,plot='Cases')

@app.route('/CancerCasesForm')
def CancerCasesForm():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT YEAR(`Date`) AS `years` FROM `rahul_Solanki` GROUP BY YEAR(`Date`) ORDER BY `Date`;'
    cur.execute(sql)
    years = []
    for row in cur:
        years.append(row['years'])
        
    return render_template('CasesForm.html', title='Filter data',years=years)

    
if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)