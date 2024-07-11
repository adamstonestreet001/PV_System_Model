# Analyze output data and compare weekly performace

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to import CSV data and convert to dataframe with datetime index
def get_data(file_path):
    df_data = pd.read_csv(file_path)
    df_data.time = pd.to_datetime(df_data.time)
    df_data['year'] = df_data.time.dt.year
    df_data['month'] = df_data.time.dt.month
    df_data['day'] = df_data.time.dt.day
    df_data['hour'] = df_data.time.dt.hour
    return df_data


if __name__ == '__main__':
    file_path20 = 'Test4OutputData_Opt_Month7_20.csv'
    file_path50 = 'Test4OutputData_Opt_Month7_50.csv'
    file_pathOpt1 = 'Test4OutputData_Opt_Month7_Opt1.csv'
    file_pathOpt2 = 'Test4OutputData_Opt_Month7_Opt2.csv'
    df_20 = get_data(file_path20)
    df_50 = get_data(file_path50)
    df_Opt1 = get_data(file_pathOpt1)
    df_Opt2 = get_data(file_pathOpt2)

    # Group Data according to preference (year, month, day)
    grouped_data20 = df_20.groupby(['year', 'month', 'day'])
    grouped_data50 = df_50.groupby(['year', 'month', 'day'])
    grouped_dataOpt1 = df_Opt1.groupby(['year', 'month', 'day'])
    grouped_dataOpt2 = df_Opt2.groupby(['year', 'month', 'day'])
    week1_20 = df_20[df_20['day'] <= 7]
    week1_50 = df_50[df_50['day'] <= 7]
    week1_Opt1 = df_Opt1[df_Opt1['day'] <= 7]
    week1_Opt2 = df_Opt2[df_Opt2['day'] <= 7]


    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']

    # graph SoC for the week:
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title('Weekly battery Levels for a 6kW System with stage 4 and 5 load shedding and optimized load profile')
    plt.xlabel('Days')
    plt.xticks(np.arange(12, 7*24, 24), days)
    plt.ylabel('Battery SoC (%)')
    plt.plot(week1_20.SoC*100, label='20% ToU Settings')
    plt.plot(week1_50.SoC*100, label='50% ToU Settings')
    plt.plot(week1_Opt1.SoC*100, label='Opt1 ToU Settings')
    plt.plot(week1_Opt2.SoC*100, label='Opt2 ToU Settings')
    plt.legend(loc='lower right')
    plt.savefig('Test4_6kWJuly_OptLoad3.png')


