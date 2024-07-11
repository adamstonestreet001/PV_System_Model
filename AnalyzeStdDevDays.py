import pandas as pd
import matplotlib.pyplot as plt



if __name__ == '__main__':
    df = pd.read_csv('NewlandsSolarData_6kW.csv')
    df.time = df.time.apply(lambda x: pd.to_datetime(f"{x[:8]} {x[9:]}", format="%Y%m%d %H%M"))
    df['year'] = df.time.dt.year
    df['month'] = df.time.dt.month
    df['day'] = df.time.dt.day
    df['hour'] = df.time.dt.hour
    production_axis_name = 'P'

    # Get the production grouped per day
    grouped_day = df.groupby(['year', 'month', 'day'])[production_axis_name]
    daily_production = grouped_day.sum()

    # Filter days that are in the range around 20 000 to 30 000:
    filtered_days = daily_production[(daily_production >= 25000) & (daily_production <= 30000)]
    std_dev_day = filtered_days.std().max()

    # Plot day in September 2019 with most std dev per day:
    sep_df = df[(df['time'].dt.year == 2019) & (df['time'].dt.month == 11)]  # Filter for September 2019
    sep_grouped = sep_df.groupby(['year', 'month', 'day'])[production_axis_name] # Group by day
    sep_daily = sep_grouped.sum()  # Sum the production per day
    sep_filtered = sep_daily[(sep_daily >= 25000) & (sep_daily <= 30000)]  # Filter for days in the range around 20 000 to 30 000

    # Get the day with the most std dev:
    sep_std_dev_day = (sep_grouped.std()).idxmax()

    #Finding a variable day
    var_day1 = grouped_day.get_group((2019, 10, 9)).values
    var_day2 = grouped_day.get_group((2019, 11, 16)).values
    var_day3 = grouped_day.get_group((2019, 11, 17)).values

    # Plotting variable days
    plt.figure(figsize=(10, 5))
    plt.xlabel('Hour')
    plt.ylabel('Production (W)')
    plt.xticks(range(0, 23, 2))
    plt.plot(var_day1)
    plt.plot(var_day2)
    plt.plot(var_day3)
    plt.legend(['2019-10-09', '2019-11-16', '2019-11-17'])
    plt.savefig('variable_days.png')