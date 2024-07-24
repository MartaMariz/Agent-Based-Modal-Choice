import pandas as pd
import pysd
import matplotlib.pyplot as plt
import ABM_model.environment as env
import ABM_model.infrastructure as infra
import utils 
from pysd.py_backend.output import ModelOutput
import time

class HybridModel:
      def __init__(self ):
         self.model = pysd.read_vensim('Vensim_model/sd_model.mdl')

         self.setSubmodels()
        
         self.pib_projection = {}
         self.getGdpProjection()
         
         road_area = self.model['Road Available']
         bus_lines = self.model['Number of Bus Routes']
         railway_lines = self.model['Number of Railway Lines']
         railway_trips = self.model['Number of Trips per Railway Line']
         bus_trips = self.model['Number of Trips per Bus Route']
         ticket_cost = self.model['Public Transport Ticket Cost']
         car_cost = self.model['CAR COST KM']
         self.abm_infra = infra.Infrastructure(road_area, bus_lines, railway_lines, railway_trips, bus_trips, ticket_cost, car_cost)
         self.__business_growth = 0
         self.__business_1 = self.model['Business structures']

      def setSubmodels(self):
         self.economy = self.model.select_submodel(vars = utils.city, exogenous_components = {'enviromental_impact_on_economy': self.model['enviromental_impact_on_economy']}, inplace=False)
         self.socioeconomic = self.model.select_submodel(vars = utils.socio_economic, exogenous_components={ 'labor_to_job_ratio' : self.model['labor_to_job_ratio'], 
                                                                                                            'business_growth': self.model['business_growth'], 'gdp_growth_rate': self.model['gdp_growth_rate']}, inplace=False)
         self.infrastruturePT = self.model.select_submodel(vars = utils.public_infrastructure, inplace=False)
         self.infrastruturePV = self.model.select_submodel(vars = utils.private_infrastructure, inplace=False)
         self.emissions_mobility = self.model.select_submodel(vars = utils.emissions_mobility_simplified, exogenous_components={  'gdp_growth_rate':self.model['gdp_growth_rate'],  
                                                                                                                     "daily railway trips":self.model["daily railway trips"], 
                                                                                                                     "daily bus trips":self.model["daily bus trips"],
                                                                                                                     "daily chosen car": self.model["daily chosen car"]}, inplace=False)
         self.emissions = self.model.select_submodel(vars = utils.emissions, exogenous_components={  "emissions of greenhouse gases mobility": self.model["emissions of greenhouse gases mobility"], 
                                                                                                   'Business structures': self.model['Business structures']}, inplace=False)
         self.indicators = self.model.select_submodel(vars = utils.indicators, exogenous_components={ 'road construction': self.model['road construction'], 'Population': self.model['Population'], 
                                                                                                     'number of trains': self.model['number of trains'], 'number of bus':self.model[ 'number of bus'],
                                                                                                   'daily chosen car':self.model['daily chosen car'], 'daily_chosen_bus': self.model['daily_chosen_bus'],
                                                                                                    'emissions_of_greenhouse_gases_mobility':self.model['emissions_of_greenhouse_gases_mobility'], 
                                                                                                    'daily_bus_capacity':self.model['daily_bus_capacity'], 'daily_chosen_railway':self.model['daily_chosen_railway'],
                                                                                               'daily_railway_capacity':self.model['daily_railway_capacity'],
                                                                                               'average monthly income 20': self.model['average monthly income 20'],
                                                                                               'Public Transport Ticket Cost': self.model['Public Transport Ticket Cost']}, inplace=False)
         
         self.output_economy = ModelOutput()
         self.output_socioeconomic = ModelOutput()
         self.output_infrastructurePT = ModelOutput()
         self.output_infrastructurePV = ModelOutput()
         self.output_emissions_mobility = ModelOutput()
         self.output_emissions = ModelOutput()
         self.output_indicators = ModelOutput()

         self.economy.set_stepper(self.output_economy,
                  step_vars=['gdpgn','enviromental_impact_on_economy'])
         self.socioeconomic.set_stepper(self.output_socioeconomic,
                  step_vars=["labor_to_job_ratio", "business_growth", "gdp_growth_rate"])
         self.infrastruturePT.set_stepper(self.output_infrastructurePT,
                  step_vars=["itbr", "itrr", "irbr","ilrr","tci"])
         self.infrastruturePV.set_stepper(self.output_infrastructurePV,
                  step_vars=["rcr", 'car_cost_km'])
         self.emissions_mobility.set_stepper(self.output_emissions_mobility,
                  step_vars=["daily_railway_trips", "daily_bus_trips", "gdp_growth_rate", "daily_chosen_car"])
         self.emissions.set_stepper(self.output_emissions,
                  step_vars=["emissions_of_greenhouse_gases_mobility", 'business_structures'])
         self.indicators.set_stepper(self.output_indicators,
                  step_vars=["road_construction", "population", "number_of_trains", "number_of_bus", 
                             "daily_chosen_car", "daily_chosen_bus",  "daily_chosen_railway","daily_walk_trips",
                             "emissions_of_greenhouse_gases_mobility", "daily_bus_capacity", "daily_railway_capacity",
                             "average_monthly_income_20", "public_transport_ticket_cost"])
                                             
                  
      def getGdpProjection(self):

         with open ('Data Preparation\data\PIB_projection.csv', 'r', encoding='utf-8-sig') as file:
            data = file.read()
            data = data.split('\n')
            for element in data:
               values = element.split(';')
               self.pib_projection[values[0]] = float(values[1])

      def getBusinessGrowth(self):
         if (self.__business_1 != self.economy['Business structures']):
            self.__business_growth = (self.economy['Business structures'] - self.__business_1) / self.__business_1
            self.__business_1 = self.economy['Business structures']
         return self.__business_growth
  
      def step(self):
         self.economy.step(1, {'gdpgn': self.pib_projection[str(self.economy.time())]})
         self.socioeconomic.step(1, {'labor_to_job_ratio': self.economy['labor_to_job_ratio'], 'business_growth': self.getBusinessGrowth(), 
                                     'gdp_growth_rate': self.economy['gdp_growth_rate']})
         
        
         if (self.economy.time() % 5 == 0):
            print("YEAR FIVE MULTIPLE")
            ticket_cost_inc = 0
            bus_trips_inc = 0
            bus_routes_inc = 0
            railway_trips_inc = 0
            railway_routes_inc = 0
            road_inc = 0

         else:
            ticket_cost_inc = 0
            bus_trips_inc = 0
            bus_routes_inc = 0
            railway_trips_inc = 0
            railway_routes_inc = 0
            road_inc = 0

         self.infrastruturePT.step(1, {'itrr': railway_trips_inc,
                                       'itbr': bus_trips_inc, 'irbr': bus_routes_inc, 'ilrr': railway_routes_inc, 'tci': ticket_cost_inc})
         self.infrastruturePV.step(1, {'rcr': road_inc, 'car_cost_km': 0.29})

         income20 = self.socioeconomic['average monthly income 20']
         income50 = self.socioeconomic['average monthly income 50']
         income90 = self.socioeconomic['average monthly income 90']
         trips = 1.607 * self.economy['Population']
         active_population = self.socioeconomic['lpf']
         ticket_cost = self.infrastruturePT['Public Transport Ticket Cost']
         car_cost = self.infrastruturePV['CAR COST KM']
         bus_trips_per_route = self.infrastruturePT['Number of Trips per Bus Route']
         railway_trips_per_line = self.infrastruturePT['Number of Trips per Railway line']
         bus_routes = self.infrastruturePT['Number of Bus Routes']
         railway_lines = self.infrastruturePT['Number of Railway Lines']
         road_area = self.infrastruturePV['Road available']

         abm = env.Environment( trips , [200, income20, income50, income90], active_population, self.abm_infra)
         
         abm.setInfrastructure(bus_trips_per_route, railway_trips_per_line, bus_routes, railway_lines, road_area)
         abm.setTicketCost(ticket_cost)
         abm.setCarCostPerKm(car_cost)
         params = [ 0.13067237,  0.60961852 ,-0.75787615, -0.51140001, -0.07634105 ,-0.41800807,
         -0.69477578, -0.56209977, -0.12861575, -0.67532208, -0.49421556, -0.31665572,
         0.18310248, -0.12728559,  0.02689007, -1.32355361]

         car_trips, bus_trips, railway_trips, walking_trips = abm.runLogit(params)  
         print("Year: ", self.economy.time())
         print("Car: {}, Bus: {}, Railway: {}, Walk: {}".format(car_trips, bus_trips, railway_trips, walking_trips))


         self.emissions_mobility.step(1, {'daily railway trips': self.infrastruturePT['Daily railway trips'], 
                                          'daily bus trips': self.infrastruturePT['Daily bus trips'], 'gdp_growth_rate': self.economy['gdp_growth_rate'],
                                          'daily chosen car': car_trips})
         
         self.emissions.step(1, {'emissions of greenhouse gases mobility': self.emissions_mobility['emissions of greenhouse gases mobility'],
                                 'Business structures': self.economy['Business structures']})
         self.indicators.step(1, {'road construction': self.infrastruturePV['road construction'], 'Population': self.economy['Population'],
                                 'number of trains': self.infrastruturePT['number of trains'], 'number of bus': self.infrastruturePT['number of bus'],
                                 'daily chosen car': car_trips, 'daily_chosen_bus': bus_trips, 'emissions_of_greenhouse_gases_mobility': self.emissions['emissions of greenhouse gases mobility'],
                                 'daily_bus_capacity': self.infrastruturePT['daily bus capacity'], 'daily_chosen_railway': railway_trips, 'daily_railway_capacity': self.infrastruturePT['daily railway capacity'],
                                 'average_monthly_income_20': self.socioeconomic['average monthly income 20'], 'public_transport_ticket_cost': self.infrastruturePT['Public Transport Ticket Cost'],
                                 'daily_walk_trips': walking_trips}
                                 
                              )
      
      def saveResults(self):
         result_economy = self.output_economy.collect(self.economy).drop(columns=['enviromental impact on economy'])
         result_socioeconomic = self.output_socioeconomic.collect(self.socioeconomic).drop(columns=['labor to job ratio', 'business growth'])
         result_infrastructurePT = self.output_infrastructurePT.collect(self.infrastruturePT)
         result_infrastructurePV = self.output_infrastructurePV.collect(self.infrastruturePV)
         result_emissions_mobility = self.output_emissions_mobility.collect(self.emissions_mobility).drop(columns=['daily chosen car', 
                                                                                                               'gdp growth rate', 'Daily railway trips', 'Daily bus trips'])
         result_emissions = self.output_emissions.collect(self.emissions).drop(columns=['Business structures', 'emissions of greenhouse gases mobility'])
         result_indicators = self.output_indicators.collect(self.indicators).drop(columns=[ 'emissions of greenhouse gases mobility', 'Population', 'road construction', 'number of trains', 'number of bus',
                                                                                           'average monthly income 20', 'Public Transport Ticket Cost', 'daily bus capacity', 'daily railway capacity'])
         

         res = result_economy.merge(result_socioeconomic, on = ['time', 'FINAL TIME', 'INITIAL TIME', 'TIME STEP', 'SAVEPER'], how = 'outer')
         res = res.merge(result_infrastructurePT, on = ['time', 'FINAL TIME', 'INITIAL TIME', 'TIME STEP', 'SAVEPER'], how = 'outer')
         res = res.merge(result_infrastructurePV, on = ['time', 'FINAL TIME', 'INITIAL TIME', 'TIME STEP', 'SAVEPER'], how = 'outer')
         res = res.merge(result_emissions_mobility, on = ['time', 'FINAL TIME', 'INITIAL TIME', 'TIME STEP', 'SAVEPER'], how = 'outer')
         res = res.merge(result_emissions, on = ['time', 'FINAL TIME', 'INITIAL TIME', 'TIME STEP', 'SAVEPER'], how = 'outer')
         res = res.merge(result_indicators, on = ['time', 'FINAL TIME', 'INITIAL TIME', 'TIME STEP', 'SAVEPER'], how = 'outer')

         res.to_csv('Results/Logit/business_as_usual.csv')                  

   
      def run(self, steps):
         for _ in range(steps):
               self.step()

         self.saveResults()



start = time.time()


hybrid = HybridModel()
hybrid.run(50)
end = time.time()
elapsed_time = end - start
print("Elapsed time: ", elapsed_time)


