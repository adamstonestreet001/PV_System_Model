import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    df_pv = pd.read_csv('testing_data_days_6kW.csv')

    # Get the testing days from data frame
    max_day = df_pv['MaxProduction'].values
    min_day = df_pv['MinProduction'].values
    var_day1 = df_pv['VariableDay1Production'].values
    ave_day = df_pv['AverageProduction'].values
    jan_day = df_pv['JanProduction'].values
    july_day = df_pv['JulyProduction'].values

    # Create a figure and axes for the plot
    plt.figure(figsize=(12, 6))
    plt.title('Days of PV energy Production used for testing', fontsize=16)
    plt.xlabel('Hour', fontsize=14)
    plt.ylabel('Production (W)', fontsize=14)
    plt.xticks(range(0, 23, 2))
    plt.grid(True, linestyle='--', linewidth=0.3)
    plt.plot(max_day, label='Max Day of Production')
    plt.plot(min_day, label='Min Day of Production')
    plt.plot(var_day1, label='Variable Day of Production')
    plt.plot(ave_day, label='Average Day of Production')
    plt.plot(jan_day, label='Average Day of Production in January')
    plt.plot(july_day, label='Average Day of Production in July')
    plt.legend()
    plt.savefig('testing_days.png')
