import sys
import pandas as pd
import numpy as np
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

import paths

def normalize_demand():
    ## Helper function to change some 2025 dates to 2024
    def change_year_to_2024(date):
        if date.year == 2025:
            return date.replace(year=2024)
        return date

    ## Read the 2-year weekly csv file
    weekly_demand_annual = pd.read_csv(paths.input_path / 'demand/Weekly_Energy_Demand_Financial_Year.csv', delimiter=',', parse_dates=['WeekStartDate'])

    ## Filter out 2023-24 RSA Contracted energy demand
    rsa_contracted_demand = weekly_demand_annual[weekly_demand_annual['Forecast_Or_Actual_Value_Legend'] == '2023-24-RSA Contracted Energy Demand']
    ## Drop Legend column
    rsa_contracted_demand = rsa_contracted_demand.drop(columns=['Forecast_Or_Actual_Value_Legend'])
    ## Reshuffle fiscal year (April to April) to calendar year (this is not a perfect method)
    rsa_contracted_demand['WeekStartDate'] = rsa_contracted_demand['WeekStartDate'].apply(change_year_to_2024)
    ## Set index and sort
    rsa_contracted_demand.set_index('WeekStartDate', inplace=True)
    rsa_contracted_demand.sort_index(inplace=True)

    ## Normalize the values
    rsa_contracted_demand['Forecast_Or_Actual_Value'] = rsa_contracted_demand['Forecast_Or_Actual_Value']/rsa_contracted_demand['Forecast_Or_Actual_Value'].sum()

    ## Read the 2-week hourly csv file
    biweekly_demand_hour = pd.read_csv(paths.input_path / 'demand/System_hourly_actual_and_forecasted_demand.csv', delimiter=',', parse_dates=['DateTimeKey'], index_col='DateTimeKey', usecols=[0,2,4]).sort_index()

    ## Combine RSA Contracted columns into new column and drop old columns
    biweekly_demand_hour['RSA Contracted'] = biweekly_demand_hour['RSA Contracted Demand'].combine_first(biweekly_demand_hour['RSA Contracted Forecast'])
    biweekly_demand_hour = biweekly_demand_hour.drop(columns=['RSA Contracted Demand', 'RSA Contracted Forecast'])

    ## Cut out a calendar week + resample series to 3h intervals
    first_monday = biweekly_demand_hour.index[biweekly_demand_hour.index.weekday == 0][0]
    end_of_week = first_monday + pd.Timedelta(days=6, hours=23, minutes=59, seconds=59)
    weekly_demand_3h = biweekly_demand_hour[first_monday:end_of_week].resample('3h').max()

    ## Normalize to year
    weekly_demand_3h_normalized = weekly_demand_3h / (weekly_demand_3h.sum() * 3)

    ## Create new array to hold the 3h values for a whole year
    normalized_demand_3h_array = np.array([])

    ## Loop through the annual array of weekly values
    for _, row in rsa_contracted_demand.iterrows():
        normalized_demand_3h_array = np.append(normalized_demand_3h_array, row['Forecast_Or_Actual_Value']*weekly_demand_3h_normalized.values.flatten())

    ## Add a final day
    avg_first_last_week = (rsa_contracted_demand.iloc[0]['Forecast_Or_Actual_Value']+rsa_contracted_demand.iloc[-1]['Forecast_Or_Actual_Value'])/2
    normalized_demand_3h_array = np.append(normalized_demand_3h_array, avg_first_last_week*weekly_demand_3h_normalized.iloc[:8].values.flatten())

    full_date_range = pd.date_range(start='2023-01-01', periods=len(normalized_demand_3h_array), freq='3h')
    normalized_demand_3h = pd.DataFrame(normalized_demand_3h_array, index=full_date_range, columns=['value'])
    normalized_demand_3h.index.name = 'timestamp'

    return normalized_demand_3h

def create_and_save_demand():
    normalize_demand().to_csv(paths.input_path / 'demand/normalized_demand.csv')
    
## Set a rate of electricity demand growth
ENERGY_DEMAND_GROWTH = 0.04

# Caluclate projected energy in MWh annually
# The parameter self_sufficiency ranges from 0 to 2 where the first 0 to 1 denotes fraction of new demand (on top of base demand) and 
def projected_energy(target_year, self_sufficiency):
    base_year = 2023
    base_demand = 20 # TWh per year
    fraction_new = min(self_sufficiency, 1)
    fraction_base = max(0, self_sufficiency - 1)

    return fraction_new * ( base_demand * (1 + ENERGY_DEMAND_GROWTH) ** (target_year - base_year) - base_demand ) + fraction_base * base_demand

if __name__ == "__main__":
    create_and_save_demand()
