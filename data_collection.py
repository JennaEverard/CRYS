import pandas as pd
import json as js
import os
import datetime

def collect_data(path, start_date, end_date, type):

    result = get_folder_contents('data/' + path + '/', start_date, end_date, type)
    return result

def get_folder_contents(folder_dir, start_date, end_date, type):

    timestamp = []
    Ne_22 = []
    Ne_22_err = []
    Ne_21 = []
    Ne_21_err = []
    Ne_20 = []
    Ne_20_err = []
    h2_center_bac = []
    ax_center_bac = []
    l2_center_bac = []

    files = os.listdir(folder_dir)
    for file in files:
        if '.' not in file:  # it's a folder
            nested_files = os.listdir(folder_dir + file)
            for nested_file in nested_files:
                if '.' in nested_file and nested_file != '.data':
                    metadata = js.load(open(folder_dir + file + '/' + nested_file, 'r'))
            for nested_file in os.listdir(folder_dir + file + '/intercepts'):
                if '.' in nested_file and nested_file != '.data':
                    intercepts = js.load(open(folder_dir + file + '/intercepts/' + nested_file, 'r'))
            for nested_file in os.listdir(folder_dir + file + '/peakcenter'):
                if '.' in nested_file and nested_file != '.data':
                    peakcenter = js.load(open(folder_dir + file + '/peakcenter/' + nested_file, 'r'))
            for nested_file in os.listdir(folder_dir + file + '/blanks'):
                if '.' in nested_file and nested_file != '.data':
                    blanks = js.load(open(folder_dir + file + '/blanks/' + nested_file, 'r'))

            msmt_date = datetime.datetime(int(metadata['timestamp'][0:4]), int(metadata['timestamp'][5:7]), int(metadata['timestamp'][8:10]))
            if metadata['analysis_type'] == type and msmt_date < end_date and msmt_date > start_date:
                timestamp.append(metadata['timestamp'])
                Ne_20.append(intercepts['Iso17.9938']['value'] - blanks['Iso17.9938']['value'])
                Ne_20_err.append(intercepts['Iso17.9938']['error'] - blanks['Iso17.9938']['error'])
                Ne_22.append(intercepts['Iso24.9938']['value'] - blanks['Iso24.9938']['value'])
                Ne_22_err.append(intercepts['Iso24.9938']['error'] - blanks['Iso24.9938']['error'])
                Ne_21.append(intercepts['Ne21']['value'] - blanks['Ne21']['value'])
                Ne_21_err.append(intercepts['Ne21']['error'] - blanks['Ne21']['error'])
                h2_center_bac.append(peakcenter['H2_CDD']['center_dac'])
                ax_center_bac.append(peakcenter['AX_CDD']['center_dac'])
                l2_center_bac.append(peakcenter['L2_CDD']['center_dac'])
    df = pd.DataFrame({
        'time': timestamp,
        '22Ne': Ne_22,
        '22_error': Ne_22_err,
        '21Ne': Ne_21,
        '21_error': Ne_21_err,
        '20Ne': Ne_20,
        '20_error': Ne_20_err,
        'H2_center_bac': h2_center_bac,
        'AX_center_bac': ax_center_bac,
        'L2_center_bac': l2_center_bac
    })

    return df

