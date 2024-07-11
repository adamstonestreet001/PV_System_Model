# Model for testing single day of the system v2 and export outputs to dataframe

import pandas as pd


# Define the function to calculate the battery level at the next timestep
def get_next_battery_level(previous_battery_level, production, consumption, is_load_shedding,
                           is_grid_charge, ToU, battery_capacity):
    excess_solar = production - consumption
    current_level = min(previous_battery_level + excess_solar, battery_capacity)
    if is_load_shedding:
        return max(0, current_level)
    else:
        min_level = ToU * battery_capacity
        if current_level < min_level:  # Battery wants to charge and will not be used.
            if is_grid_charge:
                # Uses grid to charge up to the minimum level.
                return min_level
            else:
                if excess_solar > 0:
                    return current_level
                else:
                    return min(max(previous_battery_level, current_level), min_level)
        else:  # Battery level is above minimum level.
            return min(current_level, battery_capacity)

# Function to calculate solar usage per time step:
def get_solar_usage(production, consumption, excess_solar,battery_change):
    if excess_solar < 0:
        return production
    else:
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

def sum_greater_than_zero(arr):
    sum = 0
    for element in arr:
        if element > 0:
            sum += element
    return sum

if __name__ == '__main__':
    df = pd.read_csv('TestingInputs_Test3.csv')

    # System initial conditions
    battery_capacity = 5120*2
    starting_battery_level = 0.50*battery_capacity
    starting_battery_change = 200
    consumption = df.Load.values
    is_grid_charge = df.GridCharge.values

    # Import load shedding schedule
    low_stage = df.Loadshedding_Low.values
    high_stage = df.Loadshedding_High.values
    is_load_shedding = high_stage


    # ToU Options for testing
    # ToU_10 = [0.10]*24
    ToU_20 = [0.20]*24
    ToU_50 = [0.50]*24
    # ToU_75 = [0.75]*24
    ToU_Opt1 = df.ToU_Opt1.values
    ToU_Opt2 = df.ToU_Opt2.values
    ToU = ToU_Opt1                                # Select which ToU to use

    # Import Production options for testing
    size_scaling = 6/6
    production_ave = df.AverageProduction.values
    production_july = df.JulyProduction.values
    production = production_july*size_scaling    # Select which production to use

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
    adjust_ToU_settings(ToU, is_load_shedding)

    # Calculate hourly battery levels and changes
    for i in range(n_time_increments-1):
        next_battery_level = get_next_battery_level(previous_battery_level, production[i+1], consumption[i+1],
                                                    is_load_shedding[i+1], is_grid_charge[i+1], ToU[i+1], battery_capacity)
        next_battery_levels.append(next_battery_level)
        battery_changes.append(previous_battery_level-next_battery_level)
        previous_battery_level = next_battery_level

    # Calculating hourly excess solar, solar usage and grid usage
    for i in range(n_time_increments):
        excess_solar_hourly.append(production[i]-consumption[i])
        solar_usage.append(max(0,get_solar_usage(production[i], consumption[i], excess_solar_hourly[i], battery_changes[i])))
        grid_usage.append(max(0, consumption[i]-battery_changes[i]-solar_usage[i]))
        solar_curtailment.append(max(0, production[i]-solar_usage[i]))
        SoC.append(max((next_battery_levels[i]/battery_capacity), 0))


    # Append Outputs to current dataframe
    df['BatteryLevel'] = next_battery_levels
    df['BatteryChange'] = battery_changes
    df['ExcessSolar'] = excess_solar_hourly
    df['SolarUsage'] = solar_usage
    df['SolarCurtailment'] = solar_curtailment
    df['GridUsage'] = grid_usage
    df['SoC'] = SoC
    df['New_ToU'] = ToU

    # Export dataframe to csv
    df.to_csv('Test3_Outputs_6kWJulyDay_Opt1.csv', index=False)

    # Calculate Key Results
    # total_curtailment = round(sum(solar_curtailment)*10**-3,3)
    # print("Total Curtailment =", total_curtailment)
    # total_grid_usage = round(sum(grid_usage)*10**-3,3)
    # print("Total grid usage=", total_grid_usage)
    # battery_cycle = round(sum_greater_than_zero(battery_changes)/(battery_capacity),2)
    # print("Total battery cycles =", battery_cycle)


