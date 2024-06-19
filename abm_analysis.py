import numpy as np
import scipy.optimize as opt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ABM_model.environment as env

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
    open('log.txt', 'a').write("Car: {}, Bus: {}, Railway: {}, Walk: {} --".format(p_car, p_bus, p_railway, p_walk) + str(params) + ' ' + str(error) + '\n')
    return error

   
def getWeightsLogit():   
    # income cost time (0.2 -0.4 -0.8)
    initial_params = [ 0.19603395, -0.40629409, -0.70797689 , 0.19087482, -0.510118 ,  -0.31088995,
  0.18844371, -0.4121199,  -0.31256737,  0.18699125, -0.41340016, -0.81377786]
    options = {
        'maxiter': 1000,      
        'gtol': 1e-6,         
        'disp': True        
    }

    # Optimize to find the best weights
    result = opt.minimize(objective, initial_params,  method='BFGS', options=options)

    # Extract optimized parameters
    optimized_params = result.x
    print("Optimized Parameters:", optimized_params)

    # Calculate final probabilities with optimized parameters
    final_probabilities = abm.runLogit(optimized_params)
    print("Final Probabilities - Car: {}, Bus: {}, Railway: {}, Walk: {}".format(*final_probabilities))


def getGraph(data):
    labels = data[0]
    iterations = data[1:]

    # Create a DataFrame from the iterations
    df = pd.DataFrame(iterations, columns=labels)

    # Add an iteration column
    df["iteration"] = range(1, len(df) + 1)

    # Melt the DataFrame to long format
    df_long = df.melt(id_vars="iteration", var_name="mode", value_name="count")

    # Plot using Seaborn
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_long, x="iteration", y="count", hue="mode", marker="o")
    plt.title("Convergence of Transportation Modes Over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Count")
    plt.legend(title="Mode of Transportation")
    plt.grid(True)
    plt.show()

abm = env.Environment(296010, [200, 841, 1035, 3389], 0.7)
abm.setInfrastructure(18.489)
abm.setTicketPrice(0.95)
getWeightsLogit()

