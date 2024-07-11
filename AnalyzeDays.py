# Code to extract days of production to be used for testing in the model
import pandas as pd

if __name__ == '__main__':
    # Import RAW PVGIS data and convert to dataframe with time as datetime object
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
    max_day_tuple = daily_production.idxmax()
    daily_nonzero = daily_production[daily_production > 0]
    min_day_tuple = daily_nonzero.idxmin()
    max_day_hourly = grouped_day.get_group(max_day_tuple).values
    min_day_hourly = grouped_day.get_group(min_day_tuple).values

    #Finding variable days done manually then record the date of the day selected
    var_day1 = grouped_day.get_group((2019, 10, 9)).values
    var_day2 = grouped_day.get_group((2019, 11, 16)).values

    # Getting an average day in Jan (1) and July (7) and average day over 10 year period:
    avg_day_production = df.groupby(['month', 'hour'])[production_axis_name].mean()
    avg_day_production_year = df.groupby(['hour'])[production_axis_name].mean()
    month1 = avg_day_production.xs(1, level='month')
    month7 = avg_day_production.xs(7, level='month')
    avg_month = avg_day_production_year.values

    # Exporting the testing days to csv file.
    max_data = {'Hour': range(0, len(max_day_hourly)), 'MaxProduction': max_day_hourly}
    min_data = {'MinProduction': min_day_hourly}
    jan_data = {'JanProduction': month1.values}
    july_data = {'JulyProduction': month7.values}
    avg_day_data = {'AverageProduction': avg_month}
    var_day1_data = {'VariableDay1Production': var_day1}
    var_day2_data = {'VariableDay2Production': var_day2}

    # create dataframe for each day to test:
    max_df = pd.DataFrame(max_data)
    min_df = pd.DataFrame(min_data)
    jan_df = pd.DataFrame(jan_data)
    july_df = pd.DataFrame(july_data)
    avg_day_df = pd.DataFrame(avg_day_data)
    var_day1_df = pd.DataFrame(var_day1_data)
    var_day2_df = pd.DataFrame(var_day2_data)

    combined_df = pd.concat([max_df, min_df, jan_df, july_df, avg_day_df, var_day1_df, var_day2_df], axis=1)

    # Export the combined dataframe to csv
    combined_df.to_csv('testing_data_days_6kW.csv', index=False)