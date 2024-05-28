import pysd
import matplotlib.pyplot as plt
import ABM_model.environment as env
from pysd.py_backend.output import ModelOutput

class HybridModel:
      def __init__(self):
         self.model = pysd.read_vensim('SD_model\\vensim_model.mdl')
         
         self.output = ModelOutput()
         self.model.set_stepper(self.output,
                  step_vars=["daily_chosen_car", "daily_chosen_bus"])
   
      def step(self):
            

         income25 = self.model['average monthly income 25']
         income50 = self.model['average monthly income 50']
         income95 = self.model['average monthly income 95']
         trips = 1.607 * self.model['Population']

         active_population = self.model['jobs'] / self.model['Population']
         abm = env.Environment( trips , [200, income25, income50, income95], active_population,1, 1)

         total_car, total_bus, total_railway, total_walk = abm.run()
         self.model.step(1, {"daily_chosen_car": total_car, "daily_chosen_bus": total_bus})

   
      def run(self, steps):
         for _ in range(steps):
               self.step()
         
         result_df = self.output.collect(self.model)
         print(result_df['DAILY CHOSEN CAR'])
         print(result_df['BUS Daily Occupancy rate']) 
         plt.plot(result_df['DAILY CHOSEN BUS'])
         plt.show()

hybrid = HybridModel()
hybrid.run(5)