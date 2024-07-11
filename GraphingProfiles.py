# Graphing hourly consumption patterns with average day of solar production

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # Read in the data frames
    df_loads = pd.read_csv('ConsumptionPatterns.csv')
    df_solar_days = pd.read_csv('testing_data_days_6kW.csv')

    # Get the profiles from data frames
    unopt_load = df_loads['Unoptimized'].values
    opt_load = df_loads['Opt1'].values
    ave_solar = df_solar_days['AverageProduction'].values
    ave_solar_total = ave_solar.sum()
    ave_solar_frac = ave_solar/ave_solar_total

    # Create a figure and axes for the histograms
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title('Hourly Consumption and Production Profiles')
    plt.xlabel('Hour')
    plt.ylabel('Fraction of Daily Consumption/Production')
    plt.xticks(range(0, 23, 2))
    plt.grid(True, linestyle='--', linewidth=0.3)

    # Define the x-positions for the bars
    x = np.arange(24)

    # Plot Bar Graph for the load profiles
    width = 0.3  # Width of the bars
    ax.bar(x - width, unopt_load, width=width, alpha=1, label='Unoptimized Load Profile', color='blue')
    ax.bar(x, opt_load, width=width, alpha=1, label='Optimized Load Profile', color='green')
    ax.bar(x + width, ave_solar_frac, width=width, alpha=1, label='Average Solar Production', color='orange')

    plt.legend()

    # Save the bar plot
    plt.savefig('Profiles.png')