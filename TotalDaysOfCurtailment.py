# Python script to calculate the total days of curtailment for the system model

import pandas as pd


if __name__ == '__main__':
    # Import Solar Data
    df_SolarData = pd.read_csv('NewlandsSolarData_6kW.csv')
    df_SolarData.time = df_SolarData.time.apply(lambda x: pd.to_datetime(f"{x[:8]} {x[9:]}", format="%Y%m%d %H%M"))
    df_SolarData['year'] = df_SolarData.time.dt.year
    df_SolarData['month'] = df_SolarData.time.dt.month
    df_SolarData['day'] = df_SolarData.time.dt.day
    df_SolarData['hour'] = df_SolarData.time.dt.hour
    production_axis_name = 'P'

    # Group Solar Data by day
    df_2019 = df_SolarData[df_SolarData.year == 2019]
    df_2019_day = df_2019.groupby(['year', 'month', 'day'])[production_axis_name]

    # Get the total number of days with production greater than total load between 06:00 and 19:00
    battery_capacity = 2 * 5120  # 2 x 5.120kWh batteries
    total_load = 22000 + 0.5*battery_capacity      # Total load between 06:00 and 19:00 plus energy to charge batteries
    count = 0
    for key in df_2019_day.indices.keys():
        if df_2019_day.get_group(key).sum() > total_load:
            count += 1
    print(f"Total number of days with production greater than total load: {count} days")

    # Calculate the total curtailment reduction
    battery_capacity_kW = 2 * 5.120  # 2 x 5.120kWh batteries
    headroom = 0.3          # 30% headroom
    unit_cost = 2.55        # R/kWh
    total_curtailment_reduction = round(count * battery_capacity_kW * headroom)
    print(f"Total battery capacity: {battery_capacity_kW}kWh")
    print(f"Total load: {total_load*10**-3}kWh")
    print(f"Total curtailment reduction: {total_curtailment_reduction}kWh")
    total_cost_saving= round(total_curtailment_reduction * unit_cost)
    print(f"Total maximum cost saving: R{total_cost_saving}")
