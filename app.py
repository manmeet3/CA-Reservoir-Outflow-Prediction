# -*- coding: utf-8 -*-
# Manmeet Singh
# December 9, 2019
# CMPE 256

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import date
import pickle

app = Flask(__name__)
global flag, table, prophet_outflow, prophet_storage, model_pop_usage

def import_csv():
    global table
    print("Loading csv")
    table = pd.read_csv('pop_usage.csv', low_memory=False)
    table.fillna(0, inplace=True)

def import_models():
    global prophet_outflow
    prophet_outflow = pickle.load(open('models/outlfow_phrophet.pkl', 'rb'))
    return

@app.before_first_request
def load_csvs_models():
    print("Before first request")
    import_csv()
    import_models()

@app.route('/', methods = ['GET', 'POST'])
def predict():
    global table
    pop = None
    if request.method == 'POST':
        pop = request.args.get('pop', default = 40000000, type = int)
    else:
        print ("get called")

    if pop == None:
        pop = 50000000
    else:
        pop = int(num)
    print('pop  : %s'% pop)

    # TODO: convert import_csv to put these values into a global list of lists
    hist_year = table['Year']
    hist_pop = table['Pop']
    hist_usage = table['UrbanUse']
    hist_usage.tolist()
    hist_pop.tolist()
    hist_year.tolist()
    consump_data = [hist_year, hist_pop, hist_usage]
    retval = model_prophet_outflow(2)
    outflow = {'labels': retval[0], 'actuals': [], 'predicted': retval[1]}

    info = {'date':str(date.today()), 'pop':pop, 'tot_resv_strg': 5000, 'tot_outflow': 2000, 'tot_urb_usg': 3000, 'waterconv': "1 maf = ~3e11 gallons"}
    return render_template('graph.html', labels=hist_year, pop=hist_pop, usage=hist_usage, outflow=outflow, info=info)
    #return jsonify(labels=hist_year, pop=hist_pop, usage=hist_usage, info=info)

def model_prophet_outflow(num_years):
    global prophet_outflow
    # Near future predictions only
    if num_years > 10 or num_years < 1:
        return None

    outflow_forecast = prophet_outflow.make_future_dataframe(periods=num_years*12, freq='M')
    outflow_forecast = prophet_outflow.predict(outflow_forecast)
    outflow_forecast = outflow_forecast.drop_duplicates(subset=['yhat'], keep=False)

        # Returns a list of lists for values that will be plotted
    print(outflow_forecast)
    retval = [outflow_forecast['ds'].apply(lambda x: str(x).split(' ')[0]).tolist(), outflow_forecast['yhat'].tolist()]
    return retval 

def model_prophet_storage():
    # Returns a list of lists for values that will be plotted
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    app.secret_key = 'foobar' 
    app.run(debug=True)
