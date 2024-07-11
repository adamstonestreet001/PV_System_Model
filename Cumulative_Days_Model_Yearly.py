# Python script to model the cumulative performance of a rooftop PV battery system

import pandas as pd
import random as rd


# Define the function to calculate the battery level at the next timestep
def model_day(production, starting_battery_level):
    # System initial conditions
    starting_battery_change = 200

    # Initializations
    n_time_increments = len(consumption)
    next_battery_levels = [starting_battery_level]
    battery_changes = [starting_battery_change]
    solar_usage = []
    excess_solar_hourly = []
    grid_usage = []
    solar_curtailment = []
    previous_battery_level = starting_battery_level
    SoC = []

    # Adjust ToU settings based off load shedding schedule
    #adjust_ToU_settings(ToU, is_load_shedding)

    # Calculate hourly battery levels and changes
    for i in range(n_time_increments-1):
        next_battery_level = get_next_battery_level(previous_battery_level, production[i+1], consumption[i+1], is_load_shedding[i+1], is_grid_charge[i+1], ToU[i+1], battery_capacity)
        next_battery_levels.append(next_battery_level)
        battery_changes.append(previous_battery_level-next_battery_level)
        previous_battery_level = next_battery_level

    # Calculating hourly excess solar, solar usage and grid usage
    for i in range(n_time_increments):
        excess_solar_hourly.append(production[i]-consumption[i])
        solar_usage.append(max(0,get_solar_usage(production[i], consumption[i], excess_solar_hourly[i], battery_changes[i])))
        grid_usage.append(max(0, consumption[i]-battery_changes[i]-solar_usage[i]))
        solar_curtailment.append(max(0, production[i]-solar_usage[i]))
        SoC.append(next_battery_levels[i]/battery_capacity)

    # Update final battery level before end of day:
    last_battery = next_battery_levels[-1]

    # Convert lists to pandas series
    new_production = pd.Series(production)
    new_consumption = pd.Series(consumption)
    new_solar_usage = pd.Series(solar_usage)
    new_solar_curtailment = pd.Series(solar_curtailment)
    new_grid_usage = pd.Series(grid_usage)

    # Create a DataFrame from the new Series
    new_data = pd.DataFrame({
        'Production': new_production,
        'Consumption': new_consumption,
        'BatteryUsage': battery_changes,
        'SoC': SoC,
        'SolarUsage': new_solar_usage,
        'SolarCurtailment': new_solar_curtailment,
        'GridUsage': new_grid_usage
    })

    return new_data, last_battery

# Define the function to calculate the battery level at the next timestep
def get_next_battery_level(previous_battery_level, production, consumption, is_load_shedding,
                           is_grid_charge, ToU, battery_capacity):
    excess_solar = production - consumption
    current_level = min(previous_battery_level + excess_solar, battery_capacity)
    if is_load_shedding:
        return max(0, current_level)
    else:
        min_level = ToU * battery_capacity
        if current_level < min_level:   # Battery wants to charge and will not be used.
            if is_grid_charge:          # Uses grid to charge up to the minimum level.
                return min_level
            else:
                if excess_solar > 0:
                    return current_level
                else:
                    return min(max(previous_battery_level, current_level), min_level)
        else:  # Battery level is above minimum level.
            return min(current_level, battery_capacity)


# Function to calculate solar usage per time step:
def get_solar_usage(production, consumption, excess_solar, battery_change):
    if excess_solar < 0:            # All solar produced is used
        return production
    else:                           # Solar produced is used to charge battery as well as power loads
        return consumption - battery_change


def adjust_ToU_settings(ToU, is_load_shedding):
    for i in range(len(ToU)):
        if is_load_shedding[i]:
            if 5 >= i >= 1:                     # Early morning period
                ToU[i-1] = 0.4                  # Set ToU to 0.4
            if 12 <= i <= 16:                   # Midday period
                ToU[i-1] = 0.8                  # Set ToU to 0.8
            else:
                ToU[i-1] = 0.5                  # Set ToU to 0.5
            is_grid_charge[i-1] = 1             # Set grid charge to 1
    return
# Function to choose a random day from a 2-week load shedding schedule
def choose_loadshedding():
    load_shedding = []
    load_shedding = rd.choice(load_shedding_days)
    return load_shedding

# Main funciton to get the cumulative days of testing for the system model
if __name__ == '__main__':
    # Define testing period
    year_test = 2019
    month_test = 1
    day_test = 1

    # Import solar data for Newlands system 2015 - 2020 and convert time to datetime for grouping function
    df_SolarData = pd.read_csv('NewlandsSolarData_6kW.csv')
    df_SolarData.time = df_SolarData.time.apply(lambda x: pd.to_datetime(f"{x[:8]} {x[9:]}", format="%Y%m%d %H%M"))
    df_SolarData['year'] = df_SolarData.time.dt.year
    df_SolarData['month'] = df_SolarData.time.dt.month
    df_SolarData['day'] = df_SolarData.time.dt.day
    df_SolarData['hour'] = df_SolarData.time.dt.hour
    production_axis_name = 'P'

    # Define initial battery capacity and starting battery level
    battery_capacity = 5120 * 2
    first_battery_level = 0.50 * battery_capacity

    # Import the fixed inputs to be used as global variables:
    df_fixed_inputs = pd.read_csv("TestingInputs_Test5.csv")
    consumption = df_fixed_inputs.OptLoad.values                    # Select Load Profile From Inputs
    ToU = df_fixed_inputs.ToU_Opt1.values                           # Select ToU Setting From Inputs
    is_grid_charge = df_fixed_inputs.GridCharge.values

    # Import load shedding schedule
    df_ls = pd.read_csv("WeekLoadSheddingScheduleRandom.csv")
    day1_ls = df_ls.Day1.values
    day2_ls = df_ls.Day2.values
    day3_ls = df_ls.Day3.values
    day4_ls = df_ls.Day4.values
    day5_ls = df_ls.Day5.values
    day6_ls = df_ls.Day6.values
    day7_ls = df_ls.Day7.values
    day8_ls = df_ls.Day8.values
    day9_ls = df_ls.Day9.values
    day10_ls = df_ls.Day10.values
    day11_ls = df_ls.Day11.values
    day12_ls = df_ls.Day12.values
    day13_ls = df_ls.Day13.values
    day14_ls = df_ls.Day14.values
    load_shedding_days = [day1_ls, day2_ls, day3_ls, day4_ls, day5_ls, day6_ls, day7_ls, day8_ls, day9_ls, day10_ls, day11_ls, day12_ls, day13_ls, day14_ls]
    is_load_shedding = []

    # Initialize a dataframe to store the outputs
    df_output_data = pd.DataFrame(columns=['time', 'Production', 'Consumption', 'BatteryUsage', 'SoC', 'SolarUsage', 'SolarCurtailment', 'GridUsage'])

    # Slice solar production dataframe to only time period being tested:
    test_days_month = df_SolarData[(df_SolarData.year == year_test)]
    focused_grouped_days = test_days_month.groupby(['year', 'month', 'day'])[production_axis_name]

    # Iterate through each day in the time period being tested and model the day
    count_day = 1
    for key in focused_grouped_days.indices.keys():
        # Get load shedding schedule for the day
        is_load_shedding = choose_loadshedding()
        scaling_factor = 6/6            # Scale down production to 4kW if needed

        # Get day of production and feed into model_day function
        day_of_production = focused_grouped_days.get_group(key).values*scaling_factor
        new_data = model_day(day_of_production, first_battery_level)[0]
        last_battery = model_day(day_of_production, first_battery_level)[1]

        # Append df with new data
        df_output_data = pd.concat([df_output_data, new_data], ignore_index=True)

        # Update first battery level for next day
        first_battery_level = last_battery

        # iterate count
        count_day += 1

    # Append time to output data
    df_output_data['time'] = test_days_month.time.values

    # Export output data to csv
    df_output_data.to_csv('Test5OutputData_4kW_OptLoad_Opt1.csv', index=False)


