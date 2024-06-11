import pysd
import matplotlib.pyplot as plt
import ABM_model.environment as env
from pysd.py_backend.output import ModelOutput
import time


class HybridModel:
      def __init__(self):
         self.model = pysd.read_vensim('SD_model\\vensim_model.mdl')
         self.bus = 18.489
         self.pib_projection = {}
         self.getGdpProjection()
         
         self.output = ModelOutput()
         self.model.set_stepper(self.output,
                  step_vars=["daily_chosen_car", "daily_chosen_bus","average_distance_car","gdpgn"])
         
      def getGdpProjection(self):
         with open ('Data Preparation\data\PIB_projection.csv', 'r') as file:
            data = file.read()
            data = data.split('\n')
            for element in data:
               values = element.split(';')
               self.pib_projection[values[0]] = float(values[1])
  
      def step(self):
         self.bus += 1
         income25 = self.model['average monthly income 25']
         income50 = self.model['average monthly income 50']
         income95 = self.model['average monthly income 95']
         trips = 1.607 * self.model['Population']
         active_population = self.model['jobs'] / self.model['Population']
         ticket_price = self.model['ticket fare pt 10 km']


         abm = env.Environment( trips , [200, income25, income50, income95], active_population)

         abm.setTicketPrice(ticket_price)
         abm.setInfrastructure(self.bus)
         total_car, total_bus, total_railway, total_walk = abm.run()

         average_distance_car = abm.getAverageDistanceCar()

         gdp_projection = self.pib_projection[str(self.model.time())]
      
         self.model.step(1, {"daily_chosen_car": total_car, "daily_chosen_bus": total_bus, "average_distance_car": average_distance_car, 'gdpgn': gdp_projection})

   
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