# Description: This file contains the list of indicators for each category of the model.
city = [ 'housing construction', 
                'net births', 'outmigration', 'inmigration', 'Population', 'AREA', 'attractiveness from jobs multiplier', 'attractiveness from housing multiplier', 'BCN', 'BDN', 
                'BN', 'business demolition', 'business labor force multiplier', 'business land multiplier', 'Business structures', 'DN', 'HCN', 'HDN', 'households to housing ratio',
                'Housing', 'housing availability multiplier', 'housing demolition', 'housing land multiplier', 'HS', 'IMN', 'jobs', 'JPBS', 'labor force', 'labor to job ratio', 
                'land fraction occupied', 'LPBS', 'LPF', 'LPH', 'OMN', "business construction", 'ehe', 'business_construction', 'ahm', 'blfm', 'hlm', 'blm', 'ham','GDPGN']

socio_economic = ['average monthly income 90',  'average monthly income 20', 'average monthly income 50', 'income 90 multiplier', 
                'income 50 multiplier', 'average monthly income', 'income 20 multiplier', 'labor force income multiplier', 'IMI50', 'IMI90', 'IMI20',
                 "business income multiplier", "bim", "lfim","increase_amount"]

public_infrastructure = ["change to ticket cost", "Public Transport Ticket Cost", "TCI",
               "Number of Bus Routes", "Number of Trips per Bus Route", "increaing bus trips", "number of bus", "ITBR", "increasing bus routes", 'daily bus capacity', 'Daily bus trips', "MAX CAPACITY BUS", "IRBR", 'VEHICLES PER LINE','vehicles_per_route',
               "Number of Railway Lines","Number of Trips per Railway line" , "increasing railway trips", "number of trains", "ILRR", "increasing railway lines", "daily railway capacity", "Daily railway trips", "MAX CAPACITY RAILWAY" , "ITRR", "VEHICLES PER ROUTE",       
               ]
private_infrastructure = ["Road available", "road construction", "RCR", "CAR COST KM"]

indicators = ['PEDESTRIAN SIDEWALK CONSTRUCTION', "Mobility space usage", "Land Use for mobility",'PRIVATE PARKING CONSTRUCTION', 'Emissions of greenhouse gases',  
              'BUS Daily Occupancy rate', "Railway Daily Occupancy rate",  "Motorization rate number of motorized vehicles per 1000 inhabitants", 
              'number of mototized private vehicles',"tpc", "construction", "Affordability of public transport for the poorest group", "daily walk trips"]

emissions_mobility = [
                 'DIESEL PETROL RATIO',
                'car diesel co2 emissions', 'INITIAL RATIO CAR PETROL', 'percentage car diesel', 'percentage car petrol', 'INITIAL RATIO CAR DIESEL', 
                'INITIAL RATIO CAR ELECTRICITY', 'percentage car eletricity',
                'GHC CORRECTION CAR DIESEL', 'GHC CORRECTION CAR ELECTRICITY', 'GHC CORRECTION CAR PETROL', 
                'AVERAGE DISTANCE CAR', 'WELL TO TANK CO2 EMISSION CAR DIESEL', 'car activity per year', 
                'car diesel activity', 'car electricity activity', 'car electricity co2 emission', 'car petrol activity', 'car petrol co2 emission', 'ENERGY INTENSITY PER KM CAR PETROL', 
                'ENERGY INTENSITY PER KM CAR DIESEL', 
                'ENERGY INTENSITY PER KM CAR ELECTRICITY', 'TANK TO WHEEL CO2 EMISSION CAR ELECTRICITY', 'WELL TO TANK CO2 EMISSION CAR ELECTRICITY',
                'TANK TO WHEEL CO2 EMISSION CAR DIESEL', 'TANK TO WHEEL CO2 EMISSION CAR PETROL', 'WELL TO TANK CO2 EMISSION CAR PETROL',

                "WELL TO TANK CO2 EMISSION RAILWAY ELECTRICITY", 
                "railway electricity co2 emission","AVERAGE DISTANCE RAILWAY TRIP" ,
                "ENERGY INTENSITY PER KM RAILWAY ELECTRICITY" ,"TANK TO WHEEL CO2 EMISSION RAILWAY ELECTRICITY",
                 "railway activity per year","GHC CORRECTION RAILWAY ELECTRICITY",

                 "bus electricity activity" ,"bus natural gas activity", "PERCENTAGE BUS NATURAL GAS" ,"GHC CORRECTION BUS ELECTRICITY",
                "bus electricity co2 emission" ,"bus diesel co2 emission", "bus diesel activity" , "ENERGY INTENSITY PER KM BUS NATURAL GAS",
                "bus natural gas co2 emission", "ENERGY INTENSITY PER KM BUS NATURAL GAS" ,
                "TANK TO WHEEL CO2 EMISSION BUS NATURAL GAS", "TANK TO WHEEL CO2 EMISSION BUS ELECTRICITY",
                'AVERAGE DISTANCE BUS ROUTES', 'bus activity per year',  'WELL TO TANK CO2 EMISSION BUS DIESEL', 'GHC CORRECTION BUS DIESEL', 'ENERGY INTENSITY PER KM BUS DIESEL',
                'TANK TO WHEEL CO2 EMISSION BUS DIESEL',"PERCENTAGE BUS DIESEL", "PERCENTAGE BUS ELECTRICITY","WELL TO TANK CO2 EMISSION NATURAL GAS",
                'ghc_correction_bus_natural_gas', 'well_to_tank_co2_emission_bus_electricity', 'energy_intensity_per_km_bus_electricity',

                "emissions of greenhouse gases mobility",
             ]


emissions_mobility_simplified = [
                 'DIESEL PETROL RATIO',
                'car diesel co2 emissions', 'INITIAL RATIO CAR PETROL', 'percentage car diesel', 'percentage car petrol', 'INITIAL RATIO CAR DIESEL', 
                'INITIAL RATIO CAR ELECTRICITY', 'percentage car eletricity',
                'AVERAGE DISTANCE CAR', 'car activity per year', 
                'car diesel activity', 'car electricity activity', 'car electricity co2 emission', 'car petrol activity', 'car petrol co2 emission',
                "railway electricity co2 emission","AVERAGE DISTANCE RAILWAY TRIP" ,
                 "railway activity per year",
                 "bus electricity activity" ,"bus natural gas activity", 
                "bus electricity co2 emission" ,"bus diesel co2 emission", "bus diesel activity" , 
                "bus natural gas co2 emission",
                'AVERAGE DISTANCE BUS ROUTES', 'bus activity per year',"PERCENTAGE BUS DIESEL", "PERCENTAGE BUS ELECTRICITY", "PERCENTAGE BUS NATURAL GAS",
                "emission_petrol_car", "emission_diesel_car", "emission_electricity_car",
                  "emission_electricity_railway", "emission_natural_gas_bus", "emission_electricity_bus",
                  "emission_diesel_bus",
                "emissions of greenhouse gases mobility",
             ]


emissions = ['co2 capture green spaces', 'CO2 CAPTURE PER M2 BODY OF WATER', 'co2 capture sea river', 'CO2 TECHNOLOGIES CAPTURE', 
               'BODY OF WATER M2', 'GREEN AREA', 'CO2 CAPTURE PER GREEN AREA', 
              'emissions of greenhouse gases business', "EpB",
               "emissions per year"]
