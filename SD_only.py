import pysd
import matplotlib.pyplot as plt
from pysd.py_backend.output import ModelOutput
import time
import pandas as pd

class HybridModel:
        def __init__(self):
            self.model = pysd.read_vensim('SD_model\\sd_stand_alone.mdl')
            self.pib_projection = {}
            self.getGdpProjection()
            
            self.output = ModelOutput()
            self.model.set_stepper(self.output,
                    step_vars=["gdpgn","itbr", "itrr", "irbr","rcr","ilrr"])
            
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
        

            if (self.__business_1 != self.model['Business structures']):
                self.__business_growth = (self.model['Business structures'] - self.__business_1) / self.__business_1
                self.__business_1 = self.model['Business structures']
        
            gdp_projection = self.pib_projection[str(self.model.time())]

            if (self.model.time() % 5 == 0):
                railway_trips_inc = 0
                bus_trips_inc = 0
                road_inc = 0
                bus_routes_inc = 0
                railway_routes_inc = 0.05
            else:
                railway_trips_inc = 0
                bus_trips_inc = 0
                road_inc = 0
                bus_routes_inc = 0
                railway_routes_inc = 0
            
            self.model.step(1, {'gdpgn': gdp_projection, 'business growth' : self.__business_growth ,'itrr': railway_trips_inc, 'itbr': bus_trips_inc, 'irbr': bus_routes_inc, 'rcr': road_inc, 'ilrr': railway_routes_inc})

        def run(self, steps):
            for _ in range(steps):
                self.step()
            
            result_df = self.output.collect(self.model)
            print(result_df)
            result_df.to_csv('Results/results_sd_only.csv')
        
        def getResults(self):
            results_base = pd.read_csv('Results/results_sd_only.csv')
            print(results_base['Emissions of greenhouse gases'])
            print(results_base['percentage car eletricity'])
            print(results_base['Business structures'])
            print(results_base['gdp growth rate'])
            print(results_base['average monthly income 25'])
            #graph emissions

            plt.figure(figsize=(10, 6))
            plt.plot(results_base['Emissions of greenhouse gases'])
            plt.title("Emissions of Greenhouse Gases Over Time")
            plt.xlabel("Time (years)")
            plt.ylabel("Emissions of Greenhouse Gases")
            plt.grid(True)
            plt.show()

            



        

            

start = time.time()
hybrid = HybridModel()
hybrid.run(50)
end = time.time()
hybrid.getResults()
elapsed_time = end - start
print("Elapsed time: ", elapsed_time) 