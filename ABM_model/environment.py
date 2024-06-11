from mesa import Model
from agent import MyAgent
from utils.get_matrices import getDistanceMatrix, getTravelTimeRailwayMatrix, getWaitTimeRailway, getWaitTimeBus, getRoadCapacity, getTimeDistribution
import csv
import random
from collections import defaultdict
import numpy as np
import scipy.optimize as opt


class Environment(Model):
    def __init__(self, num_agents,income, active_population, incorporatePreferences = 1, learning_rate = 5):
        super().__init__()
        self.income = income
        self.num_agents = num_agents
        self.preferences = incorporatePreferences  
        self.learning_rate = learning_rate 
        self.bus_access = [0.2, 0.8]
        self.metro_access = [0.5, 0.5]
        self.time_distribution = getTimeDistribution()
        self.population = []
        self.distances_road = getDistanceMatrix()
        self.time_trip_railway = getTravelTimeRailwayMatrix()
        self.wait_time_railway = getWaitTimeRailway()
        self.road_capacity = getRoadCapacity()
        self.car_cost_per_km = 0.248
        self.setChoiceCounts()
        self.traffic_distribution = [[ [0 for col in range(24)] for col in range(12)] for row in range(12)]
        self.congestion = [[ [0 for col in range(24)] for col in range(12)] for row in range(12)]
        self.setIncomeDistribution(active_population)

    def setInfrastructure(self, bus_per_route):
        self.wait_time_bus = getWaitTimeBus(bus_per_route)
    
    def setTicketPrice(self, ticket_cost):
        self.ticket_cost = ticket_cost

    def setChoiceCounts(self):
        self.choice_counts = defaultdict(lambda: {'car': 0, 'bus': 0, 'railway': 0, 'walk': 0})

        
    def runLogit(self, w_income, w_cost, w_time):
        self.createPopulation()

        for _ in range(self.learning_rate):
            self.setChoiceCounts()
            self.stepLogitModel(w_income, w_cost, w_time)
            self.buildCongestionMatrix()
            self.displayResults(*self.getResults())
        return self.getResults()
    
    def runMatrizBased(self):
        self.createPopulation()

        for _ in range(self.learning_rate):
            self.setChoiceCounts()
            self.step()
            self.buildCongestionMatrix()
            self.displayResults(*self.getResults())
        return self.getResults()

    def setIncomeDistribution(self, active_population):
        income_distribution = [0.25, 0.70, 0.05]
        self.income_distribution =[1 - active_population] + [active_population * val for val in income_distribution]

    def createPopulation(self):
        origin_destination_matrix = self.getDestinationMatrix()
        for i in range(len(origin_destination_matrix)):
            for j in range(len(origin_destination_matrix[i])):      
                num_agents = int(origin_destination_matrix[i][j] * self.num_agents)

                for k in range(num_agents):
                    index_income = random.choices(range(4), weights=self.income_distribution)[0] 
                    bus_access = random.choices(range(2), weights=self.bus_access)[0]
                    metro_access = random.choices(range(2), weights=self.metro_access)[0]
                    time_trip = random.choices(range(24), weights=self.time_distribution)[0]
                    if (index_income == 0):
                        car_access = 0
                    else:
                        car_access = 1
                        
                    agent_id = i * 10000 + j * 100 + k
                    first_mile = random.uniform(0,1)
                    last_mile = random.uniform(0,1)
                    agent = MyAgent(self,agent_id, i, j, self.income[index_income], time_trip, first_mile, last_mile, metro_access, bus_access, car_access, 1) 
                    agent.setPreferences(self.preferences)
                    self.population.append(agent)
        
    def getDestinationMatrix(self):
        with open('ABM_model\matrices\origin_destination.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            matrix = list(reader)
            matrix = [[float(val) for val in row if val.strip()] for row in matrix]
            origin_destination_matrix = []
            for i in range(len(matrix)):
                if (matrix[i] != []):
                    origin_destination_matrix.append(matrix[i])
        return origin_destination_matrix

    def step(self):
        for agent in self.population:
            i, j, time = agent.getPos()

            agent.setPVCost(self.distances_road[i][j],self.car_cost_per_km, self.congestion[i][j][time])
            agent.setBusCost(self.wait_time_bus[i][j], self.ticket_cost, self.distances_road[i][j])
            agent.setRailwayCost(self.time_trip_railway[i][j], self.wait_time_railway[i][j], self.ticket_cost)
            agent.setWalkCost(self.distances_road[i][j])
            time, choice = agent.step()

            self.traffic_distribution[i][j][time] += 1

            if choice in self.choice_counts[i,j]:
                self.choice_counts[i,j][choice] += 1

    def stepLogitModel(self,w_income, w_cost, w_time):
        for agent in self.population:
            i, j, time = agent.getPos()

            agent.setPVLogitCost(self.distances_road[i][j],self.car_cost_per_km, self.congestion[i][j][time])
            agent.setBusLogitCost(self.wait_time_bus[i][j], self.ticket_cost, self.distances_road[i][j])
            agent.setRailwayLogitCost(self.time_trip_railway[i][j], self.wait_time_railway[i][j], self.ticket_cost)
            agent.setWalkLogitCost(self.distances_road[i][j])
        
            time, choice = agent.LMstep(w_income, w_cost, w_time)

            self.traffic_distribution[i][j][time] += 1

            if choice in self.choice_counts[i,j]:
                self.choice_counts[i,j][choice] += 1
            
    def displayResults(self, total_car, total_bus, total_railway, total_walk):
        print("Total agents: ", total_car + total_bus + total_railway + total_walk)
        print("Percentage car: ", total_car/(total_car + total_bus + total_railway + total_walk))
        print("Percentage bus: ", total_bus/(total_car + total_bus + total_railway + total_walk))
        print("Percentage railway: ", total_railway/(total_car + total_bus + total_railway + total_walk))
        print("Percentage walk: ", total_walk/(total_car + total_bus + total_railway + total_walk))


    
    def getResults(self):
        total_car = 0
        total_bus = 0
        total_railway = 0
        total_walk = 0
        for key in self.choice_counts:
            total_car += self.choice_counts[key]['car']
            total_bus += self.choice_counts[key]['bus']
            total_railway += self.choice_counts[key]['railway']
            total_walk += self.choice_counts[key]['walk']

        percentaje_car = total_car/(total_car + total_bus + total_railway + total_walk)
        percentaje_bus = total_bus/(total_car + total_bus + total_railway + total_walk)
        percentaje_railway = total_railway/(total_car + total_bus + total_railway + total_walk)
        percentaje_walk = total_walk/(total_car + total_bus + total_railway + total_walk)

        return percentaje_car, percentaje_bus, percentaje_railway, percentaje_walk
    
    def buildCongestionMatrix(self):
        for i in range(len(self.traffic_distribution)):
            for j in range(len(self.traffic_distribution[i])):
                for h in range(len(self.traffic_distribution[i][j])):
                    self.congestion[i][j][h] = self.traffic_distribution[i][j][h]/self.road_capacity[i][j]
                    self.traffic_distribution[i][j][h] = 0

    def getAverageDistanceCar(self):
        total_car_choice = 0
        total_distance = 0
        for key in self.choice_counts:
            total_car_choice += self.choice_counts[key]['car']
            total_distance += self.choice_counts[key]['car'] * self.distances_road[key[0]][key[1]]
        return total_distance/total_car_choice
    

def objective(params):

    p_car, p_bus, p_railway, p_walk = abm.runLogit(params[0], params[1], params[2])
    p_known_car = 0.689044318
    p_known_bus = 0.146875353
    p_known_railway = 0.014330929
    p_known_walk = 0.1486515
    error = (p_car - p_known_car) ** 2 + (p_bus - p_known_bus) ** 2 + (p_railway - p_known_railway) ** 2 + (p_walk - p_known_walk) ** 2
    return error

    

abm = Environment(296010, [200, 841, 1035, 3389], 0.8)
abm.setInfrastructure(18.489)
abm.setTicketPrice(0.95)
abm.runMatrizBased()

initial_params = [1, 1, 1]

# Optimize to find the best weights
#result = opt.minimize(objective, initial_params, method='Nelder-Mead')

# Extract optimized parameters
#optimized_params = result.x
#print("Optimized Parameters:", optimized_params)

# Calculate final probabilities with optimized parameters
#final_probabilities = abm.run(optimized_params)
#print("Final Probabilities - Car: {}, Bus: {}, Railway: {}, Walk: {}".format(*final_probabilities))