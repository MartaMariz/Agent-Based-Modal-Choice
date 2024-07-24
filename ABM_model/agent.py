from mesa import Agent
import random
import math

import numpy as np


class MyAgent(Agent):
    def __init__(self, environment, unique_id, start, end, income, time_trip, first_mile, last_mile, car_access, bus_access, railway_access, walk_access, a = 0.5, b = 4):
        super().__init__(unique_id, environment)
        self.id = unique_id
        self._start = start
        self._end = end
        self._income = income
        self._time_trip = time_trip
        self._first_mile = first_mile
        self._last_mile = last_mile
        self.railway_access = railway_access
        self._bus_access = bus_access
        self._walk_access = walk_access
        self._car_access = car_access
        self._a = a
        self._b = b
        self._hours_month = 170
        self._car_speed = 70
        self._bus_speed = 25
        self._walking_speed = 4.54
        self._value_of_travel_time = self.getValueOfTravelTime()
        #print("Hello from agent", unique_id, "from", start, "to", end)
    
    def getValueOfTravelTime(self):
        return self._income / self._hours_month

    def setPVCost(self, distance, cost_per_km, congestion):
        if (self._car_access == 0):
            self._car_cost = float('inf')
            return
        
        
        time_travel = (1 + self._b * congestion ** self._a) * distance / self._car_speed
        
        self._car_cost = distance * cost_per_km + time_travel * self._value_of_travel_time
    
    def setPVLogitCost(self, distance, cost_per_km, congestion):
        if (self._car_access == 0):
            self._logit_car_cost = 1
            self._logit_car_time = 1
            return
        self._logit_car_time = ((1 + self._b * congestion ** self._a) * distance / self._car_speed)/3
        self._logit_car_cost = (distance * cost_per_km) / 20
       
    
    def setBusCost(self, wait_time, ticket_cost, distance):
        if (self._bus_access == 0):
            self._bus_cost = float('inf')
            return
        self._bus_cost = ( wait_time/60 + self._first_mile / self._walking_speed + self._last_mile / self._walking_speed + distance / self._bus_speed) * self._value_of_travel_time + ticket_cost 
        
    
    def setBusLogitCost(self, wait_time, ticket_cost, distance):
        if (self._bus_access == 0):
            self._logit_bus_time = 1
            self._logit_bus_cost = 1
            return
        self._logit_bus_cost = ticket_cost/20
        self._logit_bus_time = (wait_time/60 + self._first_mile / self._walking_speed + self._last_mile / self._walking_speed + distance / self._bus_speed)/3
        if (self._logit_bus_time > 1):
            self._logit_bus_time = 1
 
        

    def setRailwayCost(self, time_trip, wait_time, ticket_cost):
        if (self.railway_access == 0):
            self._railway_cost = float('inf')
            return
        self._railway_cost = ((time_trip/60 + wait_time/60 + self._first_mile / self._walking_speed + self._last_mile / self._walking_speed) * self._value_of_travel_time + ticket_cost)

    def setRailwayLogitCost(self, time_trip, wait_time, ticket_cost):
        

        if (self.railway_access == 0 or time_trip == float('inf')):
            self._logit_railway_time = 1
            self._logit_railway_cost = 1
            return
        self._logit_railway_cost = ticket_cost/20
        self._logit_railway_time = (time_trip/60 + wait_time/60 + self._first_mile / self._walking_speed + self._last_mile / self._walking_speed)/3
        

    def setWalkCost(self, distance):
        self._walk_cost = (distance / self._walking_speed * self._value_of_travel_time) 
    
    def setWalkLogitCost(self, distance):
        self._logit_walk_cost = 0
        if (distance / self._walking_speed > 3):
            self._logit_walk_time = 1
            return
        self._logit_walk_time = (distance / self._walking_speed)/3

    def getPos(self):
        return self._start, self._end, self._time_trip
    
    def step(self, epsilon):
        p = np.random.random() 
        if p < epsilon: 
            j = np.random.choice(4)
            if j == 0:
                return self._time_trip,"car"
            elif j == 1:
                return self._time_trip,"bus"
            elif j == 2:
                return self._time_trip,"railway"
            else:
                return self._time_trip,"walk"
        else: 
            if (self._car_cost < self._bus_cost and self._car_cost < self._railway_cost and self._car_cost < self._walk_cost):
                return self._time_trip,"car"
            elif (self._bus_cost < self._railway_cost and self._bus_cost < self._walk_cost):
                return self._time_trip,"bus"
            elif (self._railway_cost < self._walk_cost ):
                return self._time_trip,"railway"
           
            return self._time_trip,"walk"   
    
    def getUtilities(self,params):
        self.normalized_income = self._income / 20000

        if (self.normalized_income>1):
            print("ATTENTION INCOME")
        if(self._logit_car_cost>1):
            print("ATTENTION CAR COST")
        if(self._logit_car_time>1):
            print("ATTENTION CAR TIME")
        if(self._logit_bus_cost>1):
            print("ATTENTION BUS COST")
        if(self._logit_bus_time>1):
            print("ATTENTION BUS TIME")
        if(self._logit_railway_cost>1):
            print("ATTENTION RAILWAY COST")
        if(self._logit_railway_time>1):
            print("ATTENTION RAILWAY TIME")
        if(self._logit_walk_cost>1):
            print("ATTENTION WALK COST")
        if(self._logit_walk_time>1):
            print("ATTENTION WALK TIME")
        w_car, w_income_car, w_cost_car, w_time_car, w_bus, w_income_bus, w_cost_bus, w_time_bus, w_railway, w_income_railway, w_cost_railway, w_time_railway, w_walk, w_income_walk, w_cost_walk, w_time_walk = params
        utility_car = (w_car + w_income_car * self.normalized_income + w_cost_car * self._logit_car_cost + w_time_car * self._logit_car_time) 
        utility_bus = (w_bus + w_income_bus * self.normalized_income + w_cost_bus * self._logit_bus_cost + w_time_bus * self._logit_bus_time) 
        utility_railway = (w_railway + w_income_railway * self.normalized_income + w_cost_railway * self._logit_railway_cost + w_time_railway * self._logit_railway_time) 
        utility_walk = (w_income_walk + w_income_walk * self.normalized_income + w_cost_walk * self._logit_walk_cost + w_time_walk * self._logit_walk_time)
        
        return utility_car, utility_bus, utility_railway, utility_walk
    
    def getProbabilities(self, utility_car, utility_bus, utility_railway, utility_walk):
        p_car = math.exp(utility_car) 
        p_bus = math.exp(utility_bus)
        p_railway = math.exp(utility_railway)
        p_walk = math.exp(utility_walk)

        sum = p_car + p_bus + p_railway + p_walk
        p_car = p_car / sum
        p_bus = p_bus / sum
        p_railway = p_railway / sum
        p_walk = p_walk / sum
        return p_car, p_bus, p_railway, p_walk

    def LMstep(self, params):
        
        utility_car, utility_bus, utility_railway, utility_walk = self.getUtilities(params)
        p_car, p_bus, p_railway, p_walk = self.getProbabilities(utility_car, utility_bus, utility_railway, utility_walk)

        row = {'id':self.id, 'Income':self.normalized_income, 'Car cost':self._logit_car_cost, 'Car time':self._logit_car_time, 'Bus cost':self._logit_bus_cost, 'Bus time':self._logit_bus_time, 'Railway cost':self._logit_railway_cost, 'Railway time':self._logit_railway_time, 'Walk cost':self._logit_walk_cost, 'Walk time':self._logit_walk_time}
        if (p_car > p_bus and p_car > p_railway and p_car > p_walk):
            return self._time_trip,"car",row
        elif (p_bus > p_railway and p_bus > p_walk):
            return self._time_trip,"bus", row
        elif (p_railway > p_walk):
            return self._time_trip,"railway", row
        return self._time_trip,"walk",row

