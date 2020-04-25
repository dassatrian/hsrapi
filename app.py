from flask import Flask, request, jsonify
import pandas as pd
import numpy

# Self-made modules
from table_lookup import *

# Init app
app = Flask(__name__)

# reading in the hsr tables
hsr_table_1 = pd.read_csv('hsr_tables/hsr_table_1.csv')
hsr_table_2 = pd.read_csv('hsr_tables/hsr_table_2.csv')
hsr_table_3 = pd.read_csv('hsr_tables/hsr_table_3.csv')
hsr_table_4 = pd.read_csv('hsr_tables/hsr_table_4.csv')

@app.route('/', methods=['POST'])
def processjson():

    # get request data
    data = request.get_json()

    category_id = str(data['category_id']) # need to force string
    energy = data['energy']
    tsfa = data['tsfa']
    sugars = data['sugars']
    sodium = data['sodium']
    protein = data['protein']
    fibre = data['fibre']

    hsr = numpy.nan # assume numpy if nan, unless proven otherwise

    if category_id == '1' or category_id == '1D' or category_id == '2' or category_id == '2D':
        hsr_energy = list(hsr_table_1['Energy content (kJ) per 100g or 100mL'])
        hsr_tsfa = list(hsr_table_1['Saturated fatty acids (g) per 100g or 100mL'])
        hsr_sugars = list(hsr_table_1['Total sugars (g) per 100g or 100mL'])
        hsr_sodium = list(hsr_table_1['Sodium (mg) per 100g or 100mL'])
    elif category_id == '3' or category_id == '3D':
        hsr_energy = list(hsr_table_2['Energy content (kJ) per 100g or 100mL'])
        hsr_tsfa = list(hsr_table_2['Saturated fatty acids (g) per 100g or 100mL'])
        hsr_sugars = list(hsr_table_2['Total sugars (g) per 100g or 100mL'])
        hsr_sodium = list(hsr_table_2['Sodium (mg) per 100g or 100mL'])
    else: # if no category_id, can't calculate!
        return jsonify({
            "hsr": hsr
            })

    # remove nans
    hsr_energy = [x for x in hsr_energy if str(x) != 'nan']
    hsr_tsfa = [x for x in hsr_tsfa if str(x) != 'nan']
    hsr_sugars = [x for x in hsr_sugars if str(x) != 'nan']
    hsr_sodium = [x for x in hsr_sodium if str(x) != 'nan']

    # need some way of quick of getting baseline points based on the table
    baseline_points = []
    baseline_points.append(index_finder(hsr_energy, energy))
    baseline_points.append(index_finder(hsr_tsfa, tsfa))
    baseline_points.append(index_finder(hsr_sugars, sugars))
    baseline_points.append(index_finder(hsr_sodium, sodium))

    # PICK MAX INDEX!!
    baseline_points.sort()

    # Step 4) Modifying Points (P and F only since we don't have V points)
    # read in p and f tables
    hsr_p = list(hsr_table_3['Protein (g) per 100g or 100mL'])
    hsr_f = list(hsr_table_3['Dietary fibre (g) per 100g or 100mL'])

    p_points = index_finder(hsr_p, protein)
    f_points = index_finder(hsr_f, fibre)

    #Step 5) Calculate Final HSR Score
    final_hsr_score = baseline_points[-1] - p_points - f_points
    hsr = hsr_table_4['Health Star Rating'][list(hsr_table_4[category_id]).index(get_closest_value(list(hsr_table_4[category_id]), final_hsr_score))]

    return jsonify({
        "hsr": hsr
        })

# Run Server
if __name__ == '__main__':
    app.run()