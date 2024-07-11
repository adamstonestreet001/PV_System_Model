# Python script to display the outputs from the system model script

import pandas as pd
import matplotlib.pyplot as plt



if __name__ == '__main__':
    df_20 = pd.read_csv('Test3_Outputs_6kWJulyDay_20.csv')
    df_50 = pd.read_csv('Test3_Outputs_6kWJulyDay_50.csv')
    df_Opt1 = pd.read_csv('Test3_Outputs_6kWJulyDay_Opt1.csv')
    df_Opt2 = pd.read_csv('Test3_Outputs_6kWJulyDay_Opt2.csv')

    # df_inputs = pd.read_csv('TestingInputs_Test1_OptLoad.csv')
    # available_production = df_inputs.Production.values

    # # Collecting useful data from inputs and outputs for system
    # production_10 = df_10.Production.values
    # solar_usage_10 = df_10.SolarUsage.values
    # solar_curtailment_10 = df_10.SolarCurtailment.values
    # grid_usage_10 = df_10.GridUsage.values
    # battery_change_10 = df_10.BatteryChange.values
    # new_ToU = df_10.New_ToU.values


    # Plot solar production, usage and curtailment of each system
    # plt.figure(figsize=(12, 6))
    # plt.grid(True, linestyle='--', linewidth=0.5)
    # plt.xlabel('Time (hours)')
    # plt.xticks(range(0, 24, 2))
    # plt.ylabel('Solar Curtailment (W)')
    # plt.plot(solar_curtailment_10, label='10% system')
    # plt.plot(available_production, label='Available production')
    # plt.legend()
    # plt.savefig('SolarCurtailment_10_50_75.png')
    #
    # # Calculate total curtailment for each system:
    # total_curtailment_10 = sum(solar_curtailment_10)/sum(production_10) * 100

    # Plot the battery levels for each system:
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title('Battery Levels for each ToU setting on an Average July Day during High Stage Loadshedding', fontsize=16)
    plt.xlabel('Time (hours)', fontsize=14)
    plt.xticks(range(0, 24, 2))
    plt.ylabel('Battery SoC (%)', fontsize=14)
    plt.plot(df_20.SoC*100, label='20% ToU settings')
    plt.plot(df_50.SoC*100, label='50% ToU settings')
    plt.plot(df_Opt1.SoC*100, label='Opt1 ToU settings')
    plt.plot(df_Opt2.SoC*100, label='Opt2 ToU settings')
    plt.legend()
    plt.savefig('BatterySoC_Test3_JulyDay.png')

    # # Savings all outputs as one CSV file
    # df_10.to_csv('OutputsDataTest3.csv', index=False)


    # Print outputs not in csv file:
    # print('Total curtailment for 10% system: {:.2f}%'.format(total_curtailment_10))
    # battery_cycle = sum(battery_change_10[battery_change_10>=0])/(5120*2)
    # print('Total battery cycles = {:.2f} cycles'.format(battery_cycle))




