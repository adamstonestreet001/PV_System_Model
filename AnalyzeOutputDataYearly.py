# Analyze output data and compare monthly performace

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

# Function to return group of data from dataframe:
def get_monthly_info(grouped_data, year):
    monthly_curtailment = []
    monthly_grid_usage = []
    monthly_solar_usage =[]
    hours_below_10 = []
    for i in range(1, 13):
        solar_curtailment = grouped_data.get_group((year, i))['SolarCurtailment'].sum()
        grid_usage = grouped_data.get_group((year, i))['GridUsage'].sum()
        solar_usage = grouped_data.get_group((year, i))['SolarUsage'].sum()
        hours = count_values_below_10(grouped_data.get_group((year, i))['SoC'].values)
        monthly_curtailment.append(solar_curtailment)
        monthly_grid_usage.append(grid_usage)
        monthly_solar_usage.append(solar_usage)
        hours_below_10.append(hours)
    new_data = pd.DataFrame({
        'Month': range(1, 13),
        'SolarCurtailment': monthly_curtailment,
        'GridUsage': monthly_grid_usage,
        'SolarUsage': monthly_solar_usage,
        'HoursBelow10': hours_below_10
    })
    return new_data

def count_values_below_10(SoC):
    count = 0
    for i in range(len(SoC)):
        if SoC[i] < 0.1:
            count += 1
    return count

def plot_hours_below10():
    # Plot Monthly hours below 10%
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title('Monthly hours below 10% SoC for 3 different systems over 2019', fontsize=16)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Hours below 10% SoC', fontsize=14)
    plt.xticks(range(1, 13), months)
    bar_width = 0.3
    plt.bar(monthly_summary_20.Month - bar_width, monthly_summary_20.HoursBelow10, label=label1, width=0.3)
    plt.bar(monthly_summary_50.Month, monthly_summary_50.HoursBelow10, label=label2, width=0.3)
    plt.bar(monthly_summary_Opt1.Month + bar_width, monthly_summary_Opt1.HoursBelow10, label=label3, width=0.3)
    plt.legend()
    plt.savefig('Test5_3SizedSystems_2019_HoursBelow10.png')
    return

def plot_monthly_curtailment():
    # Plot Solar Curtailment
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title('Monthly solar curtailment for 3 different systems over 2019', fontsize=16)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Solar Curtailment (kWh)', fontsize=14)
    plt.xticks(range(1, 13), months)
    bar_width = 0.3
    plt.bar(monthly_summary_20.Month - bar_width, monthly_summary_20.SolarCurtailment*scaling, label=label1, width=0.3)
    plt.bar(monthly_summary_50.Month, monthly_summary_50.SolarCurtailment*scaling, label=label2, width=0.3)
    plt.bar(monthly_summary_Opt1.Month + bar_width, monthly_summary_Opt1.SolarCurtailment*scaling, label=label3, width=0.3)
    plt.legend(loc='upper center')
    plt.savefig('Test5_3SizedSystems_2019_MonthlyCurtailment.png')
    return

def plot_monthly_grid_usage():
    # Plot Monthly grid usage
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title('Monthly grid usage for 3 different systems over 2019', fontsize=16)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Grid Usage (kWh)', fontsize=14)
    plt.xticks(range(1, 13), months)
    bar_width = 0.3
    plt.bar(monthly_summary_20.Month - bar_width, monthly_summary_20.GridUsage*scaling, label=label1, width=0.3)
    plt.bar(monthly_summary_50.Month, monthly_summary_50.GridUsage*scaling, label=label2, width=0.3)
    plt.bar(monthly_summary_Opt1.Month + bar_width, monthly_summary_Opt1.GridUsage*scaling, label=label3, width=0.3)
    plt.legend(loc='upper right')
    plt.savefig('Test5_3SizedSystems_2019_MonthlyGridUsage.png')
    return

def plot_monthly_solar_usage():
    # Plot Monthly solar usage
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title('Monthly solar usage for 3 different systems over 2019', fontsize=16)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Solar Usage (kWh)', fontsize=14)
    plt.xticks(range(1, 13), months)
    bar_width = 0.3
    plt.bar(monthly_summary_20.Month - bar_width, monthly_summary_20.SolarUsage*scaling, label=label1, width=0.3)
    plt.bar(monthly_summary_50.Month, monthly_summary_50.SolarUsage*scaling, label=label2, width=0.3)
    plt.bar(monthly_summary_Opt1.Month + bar_width, monthly_summary_Opt1.SolarUsage*scaling, label=label3, width=0.3)
    plt.legend(loc='upper center')
    plt.savefig('Test5_3SizedSystems_2019_MonthlySolarUsage.png')

if __name__ == '__main__':
    output_data20 = get_data('Test5OutputData_6kW_OptLoad_Opt1.csv')
    output_data50 = get_data('Test5OutputData_4kW_OptLoad_Opt1.csv')
    output_dataOpt1 = get_data('Test5OutputData_6kW_UnOptLoad_50.csv')
    # output_data_final = get_data('Test5OutputData_6kW_UnOptLoad_Opt1.csv')


    # Group Data according to preference (year, month, day) (using monthly grouping in this)
    grouped_data20 = output_data20.groupby(['year', 'month'])
    grouped_data50 = output_data50.groupby(['year', 'month'])
    grouped_dataOpt1 = output_dataOpt1.groupby(['year', 'month'])
    # grouped_data_final = output_data_final.groupby(['year', 'month'])

    # Get monthly curtailment data
    monthly_summary_20 = get_monthly_info(grouped_data20, 2019)
    monthly_summary_50 = get_monthly_info(grouped_data50, 2019)
    monthly_summary_Opt1 = get_monthly_info(grouped_dataOpt1, 2019)
    # monthly_summary_final = get_monthly_info(grouped_data_final, 2019)


    # Month Names and labels
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    label1 = 'Optimized 6kW System'
    label2 = 'Optimized 4kW System'
    label3 = 'Unoptimized 6kW System'

    #Scaling to kWh from Wh
    scaling = 10**-3

    # Plot Monthly graphs
    plot_hours_below10()
    plot_monthly_curtailment()
    plot_monthly_grid_usage()
    plot_monthly_solar_usage()

    # Export the monthly summary data to csv
    # monthly_summary_20.to_csv('Test5OutputData_6kW_MonthlySummary_20.csv')
    # monthly_summary_50.to_csv('Test5OutputData_6kW_MonthlySummary_50.csv')
    # monthly_summary_Opt1.to_csv('Test5OutputData_6kW_MonthlySummary_Opt1.csv')
    # # monthly_summary_final.to_csv('Test5OutputData_6kW_MonthlySummary_UnOpt_Opt1.csv')



