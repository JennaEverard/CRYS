from data_collection import collect_data
from sensitivity import calc_sensitivity
from fmol_per_gram_calc import calc_fmol_per_gram
import datetime
import pandas as pd

if __name__ == "__main__":
    print("**** Loading CRYS ****")
    print("")
    print("Please provide the following inputs")
    # convert the following to input fields
    air_repo = 'Helix_air221'
    blank_repo = 'Helix_blank221'

    # Need to make it take multiple
    num_standards = 1
    standard_repos = []
    for i in range(0, num_standards):
        standard_repos.append('CRONUS')

    # need to make it only take certain dates
    num_unknowns = 1
    unk_repos = []
    for i in range(0, num_unknowns):
        unk_repos.append('GU')

    start_year = 2022
    start_month = 7
    start_day = 31
    start_date = datetime.datetime(start_year, start_month, start_day)

    end_year = 2022
    end_month = 8
    end_day = 17
    end_date = datetime.datetime(end_year, end_month, end_day)

    # AIR

    Air = collect_data(air_repo, start_date, end_date, 'air')
    print(Air)

    avg_20 = sum(Air['20Ne']) / len(Air['20Ne'])
    avg_21 = sum(Air['21Ne']) / len(Air['21Ne'])
    avg_22 = sum(Air['22Ne']) / len(Air['22Ne'])

    print("ratio 20: ", avg_20 / (avg_20 + avg_21 + avg_22))
    print("ratio 21: ", avg_21 / (avg_20 + avg_21 + avg_22))
    print("ratio 22: ", avg_22 / (avg_20 + avg_21 + avg_22))

    sensitivity = calc_sensitivity(avg_21)
    print("sensitivity: ", sensitivity / (10**14), "E14 fA/mol")
    print("sensitivity: ", sensitivity * (3000/0.5) * (1 / (1*10**15)), " cps/fmol")

    Blank_air = collect_data(blank_repo, start_date, end_date, 'blank_air')
    print(Blank_air)

    Blank_unknown = collect_data(blank_repo, start_date, end_date, 'blank_unknown')
    print(Blank_unknown)

    # NOTE: the following code is only for testing purposes
    # There were database issues, so no blank unknown exists for first sample run
    if Blank_unknown.empty:
        Blank_unknown = pd.DataFrame({
            'time': ['2022-08-01 12:14:29'],
            '22Ne': [0.20210],
            '22_error': [0.00082],
            '21Ne': [0.00353],
            '21_error': [0.00008],
            '20Ne': [1.05322],
            '20_error': [0.00142],
            'H2_center_bac': [2.38655],
            'AX_center_bac': [None],
            'L2_center_bac': [None]
        })
    print(Blank_unknown)

    print("unknown")
    for repo in unk_repos:
        unk = collect_data(repo, start_date, end_date, 'unknown')
        print(unk)

    end_date = datetime.datetime(2022, 8, 18)

    print("standard")
    for repo in standard_repos:
        std = collect_data(repo, start_date, end_date, 'unknown')
        print(std)

    calc_fmol_per_gram(std, Blank_unknown, sensitivity)


    # blank_air
    # blank_unknown
    # air

    # Unk, Air and air blank and blank unknown after aug 1, before aug 16
    # Unk, Air blank and blank unknown are in same analysis file - "analysis type" will be diff

    # CRONUS IS AUG 17 - the one outlier that needs special variable