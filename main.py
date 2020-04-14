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
  
@app.route("/process", methods=['GET','POST'])
def process():
    #request.args.get('action')
    print request.form.get('sd') 
    return 'email:'+ request.form.get('email') 

@app.route("/countByState", methods=['GET','POST'])
def countByState():   
    with open('subsetA_parking_violations_2016.csv') as f:
        data = [{k: str(v) for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

    sc ={}
    for row in data:
        st = row['Registration State']
        if st in sc.keys():
            sc[st] += 1
        else:
            sc[st] = 1
    

    sorted_sc = sorted(sc.items(),key=operator.itemgetter(1),reverse=True)
    print sorted_sc
    html = '''
    <table>
        <tr style="background-color:#eee;">
            <td>State</td>
            <td>Count</td>
        </tr>'''
        
    for row in sorted_sc:
        html += '''<tr>
            <td>'''+row[0]+'''</td>
            <td>'''+str(row[1])+'''</td>
        </tr>'''
        
    html += '''</table> '''
    return html
@app.route("/countByStateCSV", methods=['GET','POST'])
def countByStateCSV():   
    with open('subsetA_parking_violations_2016.csv') as f:
        data = [{k: str(v) for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

    sc ={}
    for row in data:
        st = row['Registration State']
        if st in sc.keys():
            sc[st] += 1
        else:
            sc[st] = 1
    

    sorted_sc = sorted(sc.items(),key=operator.itemgetter(1),reverse=True)
    print sorted_sc
    buf = 'State,Count\n'
        
    for row in sorted_sc:
        buf +=row[0]+','+str(row[1])+'\n'
        
    response = make_response(buf)
    cd = 'attachment; filename=mycsv.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response   
@app.route("/", methods=['GET','POST'])
def data():
    return '''
    <form id="myform" action="/process" method="POST">
            Enter string<br>
            <input type="text" name="email" value="123"/>
            <br><br>
            <select name="choice">
                <option value="yes">yes</option>
                <option value="no">no</option>
                <option value="not sure">not sure</option>
            </select>
            <input type="submit" value="Submit"/>
        </form>'''
    

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
