import numpy as np
import pysd
import matplotlib.pyplot as plt
from pysd.py_backend.output import ModelOutput
import time
import pandas as pd

class HybridModel:
        def __init__(self):
            self.model = pysd.read_vensim('Vensim_model\\sd_stand_alone.mdl')
            self.pib_projection = {}
            self.getGdpProjection()
            
            self.output = ModelOutput()
            self.model.set_stepper(self.output,
                    step_vars=["gdpgn","itbr", "itrr", "irbr","rcr","ilrr","daily_chosen_car", "daily_chosen_bus", "daily_chosen_railway","daily_walk_trips"])
            
            self.__business_growth = 0
            self.__business_1 = self.model['Business structures']
                    
        def getGdpProjection(self):
            with open ('Data Preparation\data\PIB_projection.csv', 'r') as file:
                data = file.read()
                data = data.split('\n')
                for element in data:
                    values = element.split(';')
                    self.pib_projection[values[0]] = float(values[1])

        def LogitModel(self):
            parameters = [-1.20668715e-03 , 1.72846114e-06 ,-1.86127391e-04 , 6.00936704e-04,
            -4.58930473e-04 ,-1.56366669e-04 , 1.34916976e-03,  4.26718618e-03,
            -1.56164667e-04, -5.97021105e-04 ,-5.59983314e-04, -9.93620043e-04,
            -1.89098066e-04, -1.66455310e-03, -4.04612682e-04] 

            utility_car = parameters[0] + parameters[1] * self.model['Road available'] + parameters[2] * self.model['CAR COST KM'] + parameters[3] * self.model['average monthly income']
            utility_bus = parameters[4] + parameters[5] * self.model['ticket fare pt 10 km'] + parameters[6] * self.model['Number of Bus Routes']  + parameters[7] * self.model['Number of Trips per Bus Route'] + parameters[8] * self.model['average monthly income']
            utility_railway = parameters[9] + parameters[10] * self.model['ticket fare pt 10 km'] + parameters[11] * self.model['Number of Railway Lines'] + parameters[12] * self.model['Number of Trips per Railway Line'] + parameters[13] * self.model['average monthly income']
            utility_walk = parameters[14]

            print(self.model['Number of Trips per Bus Route'])

            exp_U_car = np.exp(utility_car)
            exp_U_bus = np.exp(utility_bus)
            exp_U_rail = np.exp(utility_railway)
            exp_U_walk = np.exp(utility_walk)

            sum_exp_U = exp_U_car + exp_U_bus + exp_U_rail + exp_U_walk


            P_car = exp_U_car / sum_exp_U
            P_bus = exp_U_bus / sum_exp_U
            P_rail = exp_U_rail / sum_exp_U
            P_walk = exp_U_walk / sum_exp_U

            print("Car: ", P_car)
            print("Bus: ", P_bus)
            print("Railway: ", P_rail)
            print("Walk: ", P_walk)
            return P_car, P_bus, P_rail, P_walk


        def step(self):
        

            if (self.__business_1 != self.model['Business structures']):
                self.__business_growth = (self.model['Business structures'] - self.__business_1) / self.__business_1
                self.__business_1 = self.model['Business structures']
        
            gdp_projection = self.pib_projection[str(self.model.time())]

            p_car, p_bus, p_railway, p_walking = self.LogitModel()
            trips = 1.607 * self.model['Population']
            car_trips = int(trips * p_car)
            bus_trips = int(trips * p_bus)
            railway_trips = int(trips * p_railway)
            walking_trips = int(trips * p_walking)


            if (self.model.time() % 5 == 0):
                bus_trips_inc = 0
                bus_routes_inc = 0

                railway_trips_inc = 0
                railway_routes_inc = 0

                
                road_inc = 0.05
            else:
                railway_trips_inc = 0
                bus_trips_inc = 0
                road_inc = 0
                bus_routes_inc = 0
                railway_routes_inc = 0
            
            self.model.step(1, {'gdpgn': gdp_projection, 'business growth' : self.__business_growth ,'itrr': railway_trips_inc, 'itbr': bus_trips_inc, 'irbr': bus_routes_inc, 'rcr': road_inc, 'ilrr': railway_routes_inc, 'daily_chosen_car': car_trips, 'daily_chosen_bus': bus_trips, 'daily_chosen_railway': railway_trips, 'daily_walk_trips': walking_trips})

        def run(self, steps):
            for _ in range(steps):
                self.step()
            
            result_df = self.output.collect(self.model)
            print(result_df)
            result_df.to_csv('Results/results_sd_only_car_inc.csv')
        
        def getResults(self):
            results_base = pd.read_csv('Results/results_sd_only.csv')



            

            



        

            

start = time.time()
hybrid = HybridModel()
hybrid.run(50)
end = time.time()
hybrid.getResults()
elapsed_time = end - start
print("Elapsed time: ", elapsed_time) 