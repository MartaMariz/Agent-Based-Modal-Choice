import pysd
import matplotlib.pyplot as plt
import ABM_model.environment as env
from pysd.py_backend.output import ModelOutput
import time


class HybridModel:
      def __init__(self):
         self.model = pysd.read_vensim('SD_model\\vensim_model2.mdl')
         self.pib_projection = {}
         self.getGdpProjection()
         
         self.output = ModelOutput()
         self.model.set_stepper(self.output,
                  step_vars=["daily_chosen_car", "daily_chosen_bus", "daily_chosen_railway","average_distance_car","gdpgn","itbr", "itrr"])
         
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
         active_population = self.model['jobs'] / self.model['Population']
         ticket_price = self.model['ticket fare pt 10 km']
         bus_trips = self.model['Number of Trips per Bus Route']
         railway_trips = self.model['Number of Trips per Railway Line']


         abm = env.Environment( trips , [200, income25, income50, income95], active_population)

         print("Bus: ", bus_trips)
         abm.setTicketPrice(ticket_price)
         abm.setInfrastructure(bus_trips, railway_trips)
         total_car, total_bus, total_railway, total_walk = abm.runMatrixBased()

         average_distance_car = abm.getAverageDistanceCar()

         gdp_projection = self.pib_projection[str(self.model.time())]

         if (self.model.time() % 5 == 0):
            railway_trips_inc = 0.05
            bus_trips_inc = 0.05
         else:
            railway_trips_inc = 0
            bus_trips_inc = 0
         
         print("Railway trips inc: ", railway_trips_inc)
         print("Bus trips inc: ", bus_trips_inc)
      
         self.model.step(1, {"daily_chosen_car": total_car, "daily_chosen_bus": total_bus, "daily_chosen_railway": total_railway,"average_distance_car": average_distance_car, 'gdpgn': gdp_projection, 'itrr': railway_trips_inc, 'itbr': bus_trips_inc})

   
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