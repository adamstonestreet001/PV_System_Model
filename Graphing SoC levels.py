
import pandas as pd
import matplotlib.pyplot as plt



if __name__ == '__main__':
    # Import data from csv files:
    df_20 = pd.read_csv('Test2_Outputs_2kWJan_20.csv')
    df_50 = pd.read_csv('Test2_Outputs_2kWJan_50.csv')
    df_Opt1 = pd.read_csv('Test2_Outputs_2kWJan_Opt1.csv')
    df_Opt2 = pd.read_csv('Test2_Outputs_2kWJan_Opt2.csv')

    # Import data from variable day:
    df_20_var = pd.read_csv('Test2_Outputs_2kWVar1_20.csv')
    df_50_var = pd.read_csv('Test2_Outputs_2kWVar1_50.csv')
    df_Opt1_var = pd.read_csv('Test2_Outputs_2kWVar1_Opt1.csv')
    df_Opt2_var = pd.read_csv('Test2_Outputs_2kWVar1_Opt2.csv')

    # Set labels for graphs:
    system_size = 2
    label_jan = f'Battery Levels for each ToU setting for an Average day in January for a {system_size}kW system'
    label_var = f'Battery Levels for each ToU setting for a Variable day for a {system_size}kW system'


    # Plot the battery levels for Jan system:
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title(label_jan, fontsize=16)
    plt.xlabel('Time (hours)', fontsize=14)
    plt.xticks(range(0, 24, 2))
    plt.ylabel('Battery SoC (%)', fontsize=14)
    plt.plot(df_20.SoC * 100, label='20% ToU Settings')
    plt.plot(df_50.SoC * 100, label='50% ToU Settings ')
    plt.plot(df_Opt1.SoC * 100, label='Opt1 ToU Settings')
    plt.plot(df_Opt2.SoC * 100, label='Opt2 ToU Settings')
    plt.legend()
    plt.savefig('BatterySoC_Test2_2kWJanAve.png')

    # Plot the battery levels for Variable system:
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title(label_var, fontsize=16)
    plt.xlabel('Time (hours)', fontsize=14)
    plt.xticks(range(0, 24, 2))
    plt.ylabel('Battery SoC (%)', fontsize=14)
    plt.plot(df_20_var.SoC * 100, label='20% ToU Settings')
    plt.plot(df_50_var.SoC * 100, label='50% ToU Settings ')
    plt.plot(df_Opt1_var.SoC * 100, label='Opt1 ToU Settings')
    plt.plot(df_Opt2_var.SoC * 100, label='Opt2 ToU Settings')
    plt.legend()
    plt.savefig('BatterySoC_Test2_2kWVar1.png')