
import pandas as pd
import matplotlib.pyplot as plt



if __name__ == '__main__':
    # Import data from csv files:
    df_20 = pd.read_csv('Test2_Outputs_2kWJan_20.csv')
    df_50 = pd.read_csv('Test2_Outputs_2kWJan_50.csv')
    df_Opt1 = pd.read_csv('Test2_Outputs_2kWJan_Opt1.csv')
    df_Opt2 = pd.read_csv('Test2_Outputs_2kWJan_Opt2.csv')


    # Plot the battery levels for each system:
    plt.figure(figsize=(12, 6))
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.title('Battery Levels for each ToU setting on an Average Day in January for a 4kW system')
    plt.xlabel('Time (hours)')
    plt.xticks(range(0, 24, 2))
    plt.ylabel('Battery SoC (%)')
    plt.plot(df_20.SoC * 100, label='20% ')
    plt.plot(df_50.SoC * 100, label='50% ')
    plt.plot(df_Opt1.SoC * 100, label='Opt1')
    plt.plot(df_Opt2.SoC * 100, label='Opt2')
    plt.legend()
    plt.savefig('BatterySoC_Test2_Jan_4kW.png')

