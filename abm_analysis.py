import math
import numpy as np
import scipy.optimize as opt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ABM_model.environment as env
import ABM_model.infrastructure as infra

def objective(params):
    p_car, p_bus, p_railway, p_walk = abm_2017.runLogit(params)
    print("2017 Car: {}, Bus: {}, Railway: {}, Walk: {}".format(p_car, p_bus, p_railway, p_walk))
    p_known_car = 0.689044318
    p_known_bus = 0.146875353
    p_known_railway = 0.014330929
    p_known_walk = 0.1486515

    p_car2011, p_bus2011, p_railway2011, p_walk2011 = abm_2011.runLogit(params)
    print("2011 Car: {}, Bus: {}, Railway: {}, Walk: {}".format(p_car2011, p_bus2011, p_railway2011, p_walk2011))


    p_pt2011 = p_bus2011 + p_railway2011
    p_known_car2011 = 0.597
    p_known_PT2011 = 0.266
    p_known_walk2011 = 0.129  


    error = ((p_car - p_known_car) ** 2 + (p_bus - p_known_bus) ** 2 + (p_railway - p_known_railway) ** 2 + (p_walk - p_known_walk) ** 2)/4 + ((p_pt2011 - p_known_PT2011) ** 2 + (p_car2011 - p_known_car2011) ** 2 + (p_walk2011 - p_known_walk2011) ** 2)/3
    
    log_likelihood_2017 = (
        np.log(p_car) * p_known_car +
        np.log(p_bus) * p_known_bus +
        np.log(p_railway) * p_known_railway +
        np.log(p_walk) * p_known_walk
    )
    
    # Calculate log-likelihood for 2011 data
    log_likelihood_2011 = (
        np.log(p_car2011) * p_known_car2011 +
        np.log(p_pt2011) * p_known_PT2011 +  # Sum of bus and railway for PT
        np.log(p_walk2011) * p_known_walk2011
    )

    # Combine log-likelihoods
    total_log_likelihood = log_likelihood_2017 + log_likelihood_2011

    # Since we want to minimize the objective function, we return the negative log-likelihood
    
    print("Params: ", params)
    print("Log-Likelihood: ", total_log_likelihood)
    print("Error: ", error)
    file = open("Parameter estimation/log_2011-2017--error.txt", "a")
    file.write("2011 Car: {}, Bus: {}, Railway: {}, Walk: {}".format(p_car2011, p_bus2011, p_railway2011, p_walk2011) + " --- Params: " + str(params) + "Error: " + str(error) + " Log-Likelihood: " + str(total_log_likelihood) + "\n")
    return error

def getWeightsLogit():
    # income cost time
    initial_params =  [ 0.13067237,  0.60961852 ,-0.75787615 ,-0.51140001, -0.07634105, -0.41800807,
 -0.69477578 ,-0.56209977, -0.12861575, -0.67532208 ,-0.49421556, -0.31665572,
  0.18310248, -0.12728559,  0.02689007, -1.32355362]

    result = opt.minimize(objective, initial_params,  method='BFGS')

    optimized_params = result.x
    print("Optimized Parameters:", optimized_params)
    return optimized_params
    

def getGraph(data):

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data)
    plt.title('Results of car choice per iteration', fontsize=16)
    plt.xlabel('Iteration', fontsize=14)
    plt.ylabel('Number of Car Trips', fontsize=14)

    plt.savefig('Graphs/abm_results2.png', format='png')

    

abm_infra = infra.Infrastructure(400000, 94 ,2, 75 ,18.489, 0.9, 0.268)


abm_infra = infra.Infrastructure(400000, 94 ,2, 75 ,18.489, 0.9, 0.268)
params =  [ 0.31954149, -0.96154879, -0.42939921,
                       -0.65376285, -0.75320337, -0.54460689,
                        -0.52843363, -0.3677971,  -0.52260727,
                          -0.161728,    0.57288873, -0.83275606]

abm_2011 = env.Environment(263702.2, [200, 566, 744, 3237], 0.696, abm_infra)
abm_2011.setInfrastructure(18.489, 75, 94, 2, 400000)
abm_2011.setTicketCost(0.5575)
abm_2011.setCarCostPerKm(0.2437)

abm_2017 = env.Environment(263702.2, [200, 631, 782, 3526], 0.696, abm_infra)
abm_2017.setInfrastructure(18.489, 75, 94, 2, 400000)
abm_2017.setTicketCost(0.785)
abm_2017.setCarCostPerKm(0.26)

params = getWeightsLogit()



abm_2021 = env.Environment(165675 * 1.607 , [200, 752, 919, 3526], 0.662, abm_infra, epsilon=0.1)

abm_2021.setInfrastructure(18.489, 75, 94, 2, 400000)
abm_2021.setTicketCost(0.66)
abm_2021.setCarCostPerKm(0.268 )

car, bus, railway, walk = abm_2021.runLogit(params)
total = car + bus + railway + walk
p_car = car / total
p_bus = bus / total
p_railway = railway / total
p_walk = walk / total
print("2021 Car: {}, Bus: {}, Railway: {}, Walk: {}".format(p_car, p_bus, p_railway, p_walk))


res_car = 0.652
res_pt = 0.227
res_walk = 0.111

error_car = abs(p_car - res_car) /res_car
error_pt = abs(p_bus + p_railway - res_pt)/ res_pt
error_walk = abs(p_walk - res_walk)/ res_walk

mape = (error_car + error_pt + error_walk) / 3

print("MAPE: ", mape)
print("Error Car: ", error_car)
print("Error PT: ", error_pt)
print("Error Walk: ", error_walk)



