import pysd
import matplotlib.pyplot as plt
import ABM_model.environment as env
import ABM_model.infrastructure as infra
from pysd.py_backend.output import ModelOutput
import time


class HybridModel:
      def __init__(self):
         self.model = pysd.read_vensim('SD_model\\vensim_model.mdl')
         self.pib_projection = {}
         self.getGdpProjection()
         
         self.output = ModelOutput()
         self.model.set_stepper(self.output,
                  step_vars=["daily_chosen_car", "daily_chosen_bus", "daily_chosen_railway","average_distance_car","gdpgn","itbr", "itrr", "irbr","rcr"])
         
         road_area = self.model['Road Available']
         bus_lines = self.model['Number of Bus Routes']
         railway_lines = self.model['Number of Railway Lines']
         railway_trips = self.model['Number of Trips per Railway Line']
         bus_trips = self.model['Number of Trips per Bus Route']
         ticket_cost = 0.9 #self.model['ticket fare pt 10 km']
         car_cost = 0.268
         self.abm_infra = infra.Infrastructure(road_area, bus_lines, railway_lines, railway_trips, bus_trips, ticket_cost, car_cost)
         self.__business_growth = 0
         self.__business_1 = self.model['Business structures']
                  
      def getGdpProjection(self):
         with open ('Data Preparation\data\PIB_projection.csv', 'r') as file:
            data = file.read()
            data = data.split('\n')
            for element in data:
               values = element.split(';')
               self.pib_projection[values[0]] = float(values[1])
  
      def step(self):
         income25 = self.model['average monthly income 25']
         income50 = self.model['average monthly income 50']
         income95 = self.model['average monthly income 95']
         trips = 1.607 * self.model['Population']
         active_population = self.model['LPF']
         ticket_price = self.model['ticket fare pt 10 km']
         bus_trips = self.model['Number of Trips per Bus Route']
         railway_trips = self.model['Number of Trips per Railway Line']
         bus_routes = self.model['Number of Bus Routes']
         road_area = self.model['Road Available']
         print("Population: ", trips)
         print("Active population: ", active_population)
         print("Income 25: ", income25)
         print("Income 50: ", income50)
         print("Income 95: ", income95)
         print("average income ", self.model['average monthly income'])
         print("gdp growth rate: ", self.model['GDP growth rate'])


         if (self.__business_1 != self.model['Business structures']):
            self.__business_growth = (self.model['Business structures'] - self.__business_1) / self.__business_1
            self.__business_1 = self.model['Business structures']
         print("Business growth: ", self.__business_growth)
             


         abm = env.Environment( trips , [200, income25, income50, income95], active_population, self.abm_infra)
         abm.setCost(0, 0)
         abm.setInfrastructure(bus_trips, railway_trips, bus_routes, road_area)

         total_car, total_bus, total_railway, total_walk = abm.runMatrixBased()
         total = total_car + total_bus + total_railway + total_walk
         print("Total car: ", total_car/total)
         print("Total bus: ", total_bus/total)
         print("Total railway: ", total_railway/total)
         print("Total walk: ", total_walk/   total)

         average_distance_car = abm.getAverageDistanceCar()

         gdp_projection = self.pib_projection[str(self.model.time())]

         if (self.model.time() % 5 == 0):
            railway_trips_inc = 0
            bus_trips_inc = 0
            road_inc = 0
            bus_routes_inc = 0
         else:
            railway_trips_inc = 0
            bus_trips_inc = 0
            road_inc = 0
            bus_routes_inc = 0
         
      
      
         self.model.step(1, {"daily_chosen_car": total_car, "daily_chosen_bus": total_bus, "daily_chosen_railway": total_railway,"average_distance_car": average_distance_car, 'gdpgn': gdp_projection, 'business growth' : self.__business_growth ,'itrr': railway_trips_inc, 'itbr': bus_trips_inc, 'irbr': bus_routes_inc, 'rcr': road_inc})

   
      def run(self, steps):
         for _ in range(steps):
               self.step()
         
         result_df = self.output.collect(self.model)
         print(result_df)

start = time.time()
hybrid = HybridModel()
hybrid.run(50)
end = time.time()
elapsed_time = end - start
print("Elapsed time: ", elapsed_time) 