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
    return render_template('test.html', title='Home', msg='Welcome!!!!')

@app.route('/countStates')
def countStates():
    state = request.args.get('state')
    fn = 'subsetA_parking_violations_2016.csv'
    f = open(fn,'r')
    reader = csv.reader(f)
    statehist = {}
    n=0
    for row in reader:
        if n > 0:
            if (state is not None and state == row[2]) or state is None:
                k = row[2]
                if k in statehist.keys():
                    statehist[k] += 1
                else:
                    statehist[k] = 1
            
        n+=1
    f.close()
    sorted_states = sorted(statehist.items(),key=operator.itemgetter(1),reverse=True)
    #print(sorted_states)
    #print(statehist)
    #return json.dumps(statehist)   
    s = ''
    for st in sorted_states:
        s += st[0] + ' ' + str(st[1]) + '<br>'
    return render_template('states.html', title='State count', states=sorted_states)

@app.route('/countStatesPlot')
def countStatesPlot():
    fn = 'subsetA_parking_violations_2016.csv'
    f = open(fn,'r')
    reader = csv.reader(f)
    statehist = {}
    n=0
    for row in reader:
        if n > 0:
            k = row[2]
            if k in statehist.keys():
                statehist[k] += 1
            else:
                statehist[k] = 1
            
        n+=1
    f.close()
    sorted_states = sorted(statehist.items(),key=operator.itemgetter(1),reverse=True)
    #print(sorted_states)
    #[('NY', 82606), ('NJ', 9710),
    counts = []
    states = []
    for state,count in sorted_states:
        counts.append(count)
        states.append(state)
    #print(counts,states)
    #print(statehist)
    #return json.dumps(sorted_states)   
    jsdata = {'states':states,'counts':counts}
    return render_template('statesPlot.html', title='State Plot', data=jsdata,plot='state')
@app.route('/snowDepthPlot',methods = ['GET','POST'])
def snowDepthPlot():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    qyear = request.args.get('year')
    if qyear is not None:
        sql = 'SELECT * FROM `conlontj_snow` WHERE YEAR(`Date`) = %s ORDER BY `Date`';
        cur.execute(sql,(qyear))
    else:
        sql = 'SELECT * FROM `conlontj_snow` ORDER BY `Date`';
        cur.execute(sql)
    jsx = []
    jsy = []
    
    for row in cur:
        jsx.append(row['Date'])
        jsy.append(row['Depth'])
    jsdata = {'x':jsx,'y':jsy}
    return render_template('snowPlot.html', title='Snow Plot', data=jsdata,plot='snow')

@app.route('/snowDepthForm')
def snowDepthForm():
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',
                       passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT YEAR(`Date`) AS `years` FROM `conlontj_snow` GROUP BY YEAR(`Date`) ORDER BY `Date`;'
    cur.execute(sql)
    years = []
    for row in cur:
        years.append(row['years'])
        
    return render_template('snowForm.html', title='Filter data',years=years)

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
