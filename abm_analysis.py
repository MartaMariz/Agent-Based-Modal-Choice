import numpy as np
import scipy.optimize as opt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ABM_model.environment as env
import ABM_model.infrastructure as infra

def objective(params):
    p_car, p_bus, p_railway, p_walk = abm.runLogit(params)
    print("Car: {}, Bus: {}, Railway: {}, Walk: {}".format(p_car, p_bus, p_railway, p_walk))
    p_known_car = 0.689044318
    p_known_bus = 0.146875353
    p_known_railway = 0.014330929
    p_known_walk = 0.1486515
    error = (p_car - p_known_car) ** 2 + (p_bus - p_known_bus) ** 2 + (p_railway - p_known_railway) ** 2 + (p_walk - p_known_walk) ** 2
    print("Params: ", params)
    print("Error: ", error)
    open('Parameter estimation/log.txt', 'a').write("Car: {}, Bus: {}, Railway: {}, Walk: {} --".format(p_car, p_bus, p_railway, p_walk) + str(params) + ' ' + str(error) + '\n')
    return error

   
def getWeightsLogit():
    # income cost time
    initial_params = [ 0.31954149, -0.96154879, -0.42939921,
                       -0.65376285, -0.75320337, -0.54460689,
                        -0.52843363, -0.3677971,  -0.52260727,
                          -0.161728,    0.57288873, -0.83275606]
    options = {
        'maxiter': 1000,      
        'gtol': 1e-6,         
        'disp': True        
    }
    result = opt.minimize(objective, initial_params,  method='BFGS', options=options)

    optimized_params = result.x
    print("Optimized Parameters:", optimized_params)
    final_probabilities = abm.runLogit(optimized_params)
    print("Final Probabilities - Car: {}, Bus: {}, Railway: {}, Walk: {}".format(*final_probabilities))


def getGraph(data):

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data)
    plt.title('Results of car choice per iteration', fontsize=16)
    plt.xlabel('Iteration', fontsize=14)
    plt.ylabel('Number of Car Trips', fontsize=14)

    plt.savefig('Graphs/abm_results2.png', format='png')

    

abm_infra = infra.Infrastructure(400000, 94 ,2, 75 ,18.489, 0.9, 0.268)

abm = env.Environment(296010, [200, 841, 1035, 3389], 0.7, abm_infra)
abm.setInfrastructure(18.489, 75, 94, 2, 400000)
abm.setTicketCost(0.9)
abm.setCarCostPerKm(0.268)

results = abm.runMatrixBased()

print(results)

getGraph(results)


