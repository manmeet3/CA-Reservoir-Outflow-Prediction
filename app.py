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
global flag, table, pop_dict, prophet_outflow, prophet_storage, waterforpop_model

current_year = 2019
million=1000000
maf_to_gallon = 325851428571

def import_csv():
    global table, pop_dict
    print("Loading csv")
    table = pd.read_csv('pop_usage.csv', low_memory=False)
    table.fillna(0, inplace=True)
    pop_dict = pd.read_csv('ca_pop.csv', low_memory=False)
    pop_dict = pd.Series(pop_dict.Pop.values,index=pop_dict.Year).to_dict()

def import_models():
    global prophet_outflow, waterforpop_model
    prophet_outflow = pickle.load(open('models/outlfow_phrophet.pkl', 'rb'))
    waterforpop_model = pickle.load(open('models/waterforpop_model.pkl', 'rb'))
    return

@app.before_first_request
def load_csvs_models():
    import_csv()
    import_models()

@app.route('/', methods = ['GET', 'POST'])
def predict():
    global table

    pop = request.args.get('pop', default = 40, type = int)
    year = request.args.get('year', default = 2019, type = int)

    if year != 2019 and pop == 40:
        pop = pop_dict[year]/million
    print(pop)
    # TODO: convert import_csv to put these values into a global list of lists
    hist_year = (table['Year']).tolist()
    hist_pop = (table['Pop']).tolist()
    hist_usage = (table['UrbanUse']).tolist()
    #hist_usage = hist_usage.tolist()
    #hist_pop = hist_pop.tolist()
    #hist_year = hist_year.tolist()

    hist_year.append(year)
    hist_pop.append(pop)
    predicted_maf = model_water_for_pop(pop) / 13100000000
    hist_usage.append(predicted_maf)
    retval = model_prophet_outflow(year)
    outflow = {'labels': retval[0], 'actuals': [1], 'predicted': retval[2]}
    #outflow = {'labels': [2010,2011,2012], 'actuals': [3,4,5], 'predicted': [6,7,8]}

    consump_data = [hist_year, hist_pop, hist_usage]
    tot_outflow = (max(outflow['predicted']) * 7.5 * 3600 * 24 * 365)/maf_to_gallon
    #print(outflow['predicted'])
    info = {'date': year, 'pop':round(pop,1), 'tot_resv_strg': 0, 'tot_outflow': round(tot_outflow,2), 'tot_urb_usg': round(predicted_maf, 2), 'waterconv': "1 maf = ~3e11 gallons"}

    return render_template('graph.html', labels=hist_year, pop=hist_pop, usage=hist_usage, outflow=outflow, info=info)
    #return jsonify(labels=hist_year, pop=hist_pop, usage=hist_usage, info=info)

def model_water_for_pop(population, already_million=False):
    global waterforpop_model
    if population < 1 or population > 100:
        return None
    if not already_million:
        population=population*million
    water_needed=waterforpop_model.predict([[population]])
    return water_needed[0]


def model_prophet_outflow(year):
    global prophet_outflow
    # Near future predictions only
    if year > 2040 or year < 2019:
        return None

    outflow_forecast = prophet_outflow.make_future_dataframe(periods=(year-(current_year-1))*12, freq='M')
    outflow_forecast = prophet_outflow.predict(outflow_forecast)
    outflow_forecast = outflow_forecast.drop_duplicates(subset=['yhat'], keep=False)

        # Returns a list of lists for values that will be plotted
    #print(outflow_forecast)
    dates = outflow_forecast['ds'].apply(lambda x: str(x).split(' ')[0]).tolist()
    trend_vals = outflow_forecast['trend'].apply(lambda x: abs(x)).tolist()
    predicted = outflow_forecast['yhat'].apply(lambda x: abs(x)).tolist()
    #print(trend_vals)
    retval = [dates, trend_vals, predicted]
    return retval 

def model_prophet_storage():
    # Returns a list of lists for values that will be plotted
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    app.secret_key = 'foobar' 
    app.run(debug=True)
