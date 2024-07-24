

import pandas as pd


res = pd.read_csv('Results/Logit/business_as_usual.csv')
real_income_20 = 752
real_income_50 = 919
real_income_90 = 3526

real_median_income = 962

real_population = 166900
real_business = 16118
real_housing = 74537

real_bus_occupancy = 0.101
real_railway_occupancy = 0.129

real_motorization_rate = 544 

real_electricity_distribution = 0.02

res_income_20 = res.loc[res['time'] == 2021, 'average monthly income 20']
res_income_50 = res.loc[res['time'] == 2021, 'average monthly income 50']
res_income_90=  res.loc[res['time'] == 2021, 'average monthly income 90']
res_median_income = res.loc[res['time'] == 2021, 'average monthly income']

res_population = res.loc[res['time'] == 2021, 'Population']
res_business = res.loc[res['time'] == 2021, 'Business structures']
res_housing = res.loc[res['time'] == 2021, 'Housing']

res_bus_occupancy = res.loc[res['time'] == 2021, 'BUS Daily Occupancy rate']
res_railway_occupancy = res.loc[res['time'] == 2021, 'Railway Daily Occupancy rate']
res_motorization = res.loc[res['time'] == 2021, 'Motorization rate number of motorized vehicles per 1000 inhabitants']

res_electricity_distribution = res.loc[res['time'] == 2021, 'percentage car eletricity']

res_car = res.loc[res['time'] == 2021, 'daily chosen car']
res_bus = res.loc[res['time'] == 2021, 'daily chosen bus']
res_railway = res.loc[res['time'] == 2021, 'daily chosen railway']
res_walk = res.loc[res['time'] == 2021, 'daily walk trips']

total = res_car + res_bus + res_railway + res_walk
res_pcar = res_car/total
res_ppt = res_bus/total + res_railway/total
res_prailway = res_railway/total
res_pwalk = res_walk/total

real_pcar = 0.652
real_ppt = 0.227
real_pwalk = 0.111


mape_income_20 = abs(real_income_20 - res_income_20)/real_income_20
mape_income_50 = abs(real_income_50 - res_income_50)/real_income_50
mape_income_90 = abs(real_income_90 - res_income_90)/real_income_90
mape_median_income = abs(real_median_income - res_median_income)/real_median_income

mape_population = abs(real_population - res_population)/real_population
mape_business = abs(real_business - res_business)/real_business
mape_housing = abs(real_housing - res_housing)/real_housing

mape_bus_occupancy = abs(real_bus_occupancy - res_bus_occupancy)/real_bus_occupancy
mape_railway_occupancy = abs(real_railway_occupancy - res_railway)/real_railway_occupancy
mape_motorization = abs(real_motorization_rate - res_motorization)/real_motorization_rate

mape_electricity_distribution = abs(real_electricity_distribution - res_electricity_distribution)/real_electricity_distribution

mape_car = abs(real_pcar - res_pcar)/real_pcar
mape_PT = abs(real_ppt - res_ppt)/real_ppt
mape_walk = abs(real_pwalk - res_pwalk)/real_pwalk

print("Car real: {}, Car res: {}, error {}:".format(real_pcar, res_pcar, mape_car))
print("PT real: {}, PT res: {}, error {}:".format(real_ppt, res_ppt, mape_PT))
print("Walk real: {}, Walk res: {}, error {}:".format(real_pwalk, res_pwalk, mape_walk))
print("Income 20 real: {}, Income 20 res: {}, error {}:".format(real_income_20, res_income_20, mape_income_20))
print("Income 50 real: {}, Income 50 res: {}, error {}:".format(real_income_50, res_income_50, mape_income_50))
print("Income 90 real: {}, Income 90 res: {}, error {}:".format(real_income_90, res_income_90, mape_income_90))
print("Median income real: {}, Median income res: {}, error: {}".format(real_median_income, res_median_income, mape_median_income))
print("Population real: {}, Population res: {}, error: {}".format(real_population, res_population, mape_population))
print("Business real: {}, Business res: {}, error: {}".format(real_business, res_business, mape_business))
print("Housing real: {}, Housing res: {}, error: {}".format(real_housing, res_housing, mape_housing))
print("Bus occupancy real: {}, Bus occupancy res: {}, error: {}".format(real_bus_occupancy, res_bus_occupancy, mape_bus_occupancy))
print("Railway occupancy real: {}, Railway occupancy res: {}, error: {}".format(real_railway_occupancy, res_railway_occupancy, mape_railway_occupancy))
print("Motorization real: {}, Motorization res: {}, error: {}".format(real_motorization_rate, res_motorization, mape_motorization))
print("Electricity distribution real: {}, Electricity distribution res: {}, error: {}".format(real_electricity_distribution, res_electricity_distribution, mape_electricity_distribution))

