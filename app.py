# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import date

app = Flask(__name__)
global flag, table

flag = 1
table = None

@app.route('/', methods = ['GET', 'POST'])
def predict():
    global table
    pop = None
    if request.method == 'POST':
        pop = request.args.get('pop', default = 40000000, type = int)
    else:
        print ("get called")

    global table

    if pop == None:
        pop = 50000000
    else:
        pop = int(num)
    print('pop  : %s'% pop)

    import_csv()

    hist_year = table['Year']
    hist_pop = table['Pop']
    hist_usage = table['UrbanUse']
    hist_usage.tolist()
    hist_pop.tolist()
    hist_year.tolist()

    today = str(date.today())
    info = {'date':today, 'pop':pop, 'tot_resv_strg': 5000, 'tot_outflow': 2000, 'tot_urb_usg': 3000, 'waterconv': "1 maf = ~3e11 gallons"}
    return render_template('graph.html', labels=hist_year, pop=hist_pop, usage=hist_usage, info=info)
    #return jsonify(labels=hist_year, pop=hist_pop, usage=hist_usage, info=info)

def import_csv():
    global table, flag
    if flag < 1:
        return
    print("Loading csv")
    table = pd.read_csv('pop_usage.csv', low_memory=False)
    table.fillna(0, inplace=True)
    flag = 0

if __name__ == '__main__':
    app.run(port=5000)
    app.secret_key = 'mykey' 
    app.run(debug=True)
    
#TODO: 
