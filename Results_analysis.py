import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def getDatasetsHybridLogit():
    results_base = pd.read_csv('Results/Hybrid_Logit/business_as_usual.csv')
    results_bus_lines = pd.read_csv('Results/Hybrid_Logit/bus_routes_10.csv')
    results_bus_trips = pd.read_csv('Results/Hybrid_Logit/bus_trips_10.csv')
    results_car_increase = pd.read_csv('Results/Hybrid_Logit/road_investment_10.csv')
    results_railway_trips = pd.read_csv('Results/Hybrid_Logit/railway_trips_10.csv')
    results_railway_routes = pd.read_csv('Results/Hybrid_Logit/railway_routes_10.csv')
    results_ticket_inc = pd.read_csv('Results/Hybrid_Logit/ticket_cost_inc_10.csv')
    results_ticket_dec = pd.read_csv('Results/Hybrid_Logit/ticket_cost_dec_10.csv')

    dataset_hybrid_logit = {
    'Business as Usual': results_base[1:],
    'Increase BUS lines': results_bus_lines[1:],
    'Increase BUS trips': results_bus_trips[1:],
    'Increase Road Length': results_car_increase[1:],
    'Increase Railway trips': results_railway_trips[1:],
    'Increase Railway routes': results_railway_routes[1:],
    'Increase Ticket Cost': results_ticket_inc[1:],
    'Decrease Ticket Cost': results_ticket_dec[1:]
    }   

    return dataset_hybrid_logit

def getDatasetHybridCost():
    results_base = pd.read_csv('Results/Hybrid_Matrix_Cost/business_as_usual.csv')
    results_bus_lines = pd.read_csv('Results/Hybrid_Matrix_Cost/bus_routes_10.csv')
    results_bus_trips = pd.read_csv('Results/Hybrid_Matrix_Cost/bus_trips_10.csv')
    results_car_increase = pd.read_csv('Results/Hybrid_Matrix_Cost/road_investment_10.csv')
    results_railway_trips = pd.read_csv('Results/Hybrid_Matrix_Cost/railway_trips_10.csv')
    results_railway_routes = pd.read_csv('Results/Hybrid_Matrix_Cost/railway_routes_10.csv')
    results_ticket_inc = pd.read_csv('Results/Hybrid_Matrix_Cost/ticket_cost_inc_10.csv')
    results_ticket_dec = pd.read_csv('Results/Hybrid_Matrix_Cost/ticket_cost_dec_10.csv')

    dataset_hybrid_cost = {
    'Business as Usual': results_base[1:],
    'Increase BUS lines': results_bus_lines[1:],
    'Increase BUS trips': results_bus_trips[1:],
    'Increase Road Length': results_car_increase[1:],
    'Increase Railway trips': results_railway_trips[1:],
    'Increase Railway routes': results_railway_routes[1:],
    'Increase Ticket Cost': results_ticket_inc[1:],
    'Decrease Ticket Cost': results_ticket_dec[1:]
    }   

    return dataset_hybrid_cost

def cleanResults(results):
    results = results.rename(columns={
        'daily chosen car': 'Car',
        'daily chosen bus': 'Bus',
        'daily chosen railway': 'Railway',
        'daily walk trips': 'Walk',
    }
    )
    results = results[1:]
    return results

def getTripsDistributionGraph(results, title):

    results = cleanResults(results)

    trips_data = results[['Car', 'Bus', 'Railway', 'Walk','time']]

    trips_data = trips_data.reset_index(drop=True).melt(id_vars='time', var_name='Transport', value_name='Daily Chosen')

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=trips_data, x='time', y='Daily Chosen', hue='Transport', marker='o')

    plt.title('Daily Choices of Transport Methods Over Time ' + title, fontsize=16)
    plt.xlabel('Time (years)', fontsize=14)
    plt.ylabel('Number of Trips', fontsize=14)
    plt.legend(title='Transport Method', title_fontsize='13', fontsize='11')

    plt.savefig('Graphs/transport_choices_' + title + '.png', format='png')
    plt.clf()


def compareIncome(results):
    results = cleanResults(results)
    target_data = results[['average monthly income 25', 'average monthly income 50', 'average monthly income 95', 'average monthly income', 'time']]
    
    combined_data = target_data.melt(id_vars=['time'], var_name='Income', value_name='Euros')
   
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=combined_data, x='time', y='Euros', hue='Income', markers=True, dashes=False)
    plt.title('Average Monthly Income Over Time', fontsize=16)
    plt.xlabel('Time (years)', fontsize=14)
    plt.ylabel('Average Monthly Income (Euros)', fontsize=14)


    plt.savefig('Graphs_SD_only/average_monthly_income.png', format='png')
    plt.clf()

def getVariableGraph(dir, results, title):
    results = cleanResults(results)
    target_data = results[[title, 'time']]
    sns.lineplot(data=target_data, x='time', y=title)
    plt.title( title + ' over time', fontsize=16)
    plt.xlabel('Time (years)', fontsize=14)
    plt.ylabel(title, fontsize=14)

    plt.savefig('Graphs/'+ dir + '/' + title + '.png', format='png')
    plt.clf()


     

def compareTripDistributionGraph(dir, results_base, results_comparison, title_base, title_comparison):

    results_base = cleanResults(results_base)
    results_comparison = cleanResults(results_comparison)
    trips_data_base = results_base[['Car', 'Bus', 'Railway','Walk','time']]
    trips_data_comparison = results_comparison[['Car', 'Bus', 'Railway', 'Walk','time']]
    
    trips_data_base['Dataset'] = title_base
    trips_data_comparison['Dataset'] = title_comparison

    combined_results = pd.concat([trips_data_base, trips_data_comparison])

    combined_data = combined_results.melt(id_vars=['time', 'Dataset'], var_name='Transport', value_name='Daily Chosen')

    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=combined_data, x='time', y='Daily Chosen', hue='Transport', style='Dataset', markers=True, dashes=False)

    plt.title('Daily Choices of Transport Methods Over the Years', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Choices', fontsize=14)
    plt.legend(title='Transport Method & Dataset', title_fontsize='13', fontsize='11')

    plt.savefig('Graphs/' + dir + '/compare_transport_choices_' + title_base + '-' + title_comparison + '.png', format='png')
    plt.clf()


def compareSimpleGraph(dir, results_base, results_comparison, title_base, title_comparison, variable):
    
        results_base = cleanResults(results_base)
        results_comparison = cleanResults(results_comparison)
    
        data_base = results_base[[variable, 'time']]
        data_comparison = results_comparison[[variable, 'time']]
    
        data_base = data_base.assign(Dataset=title_base)
        data_comparison = data_comparison.assign(Dataset=title_comparison)
    
        combined_results = pd.concat([data_base, data_comparison])
        
        
        sns.set(style="whitegrid")
    
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=combined_results, x='time', y=variable, hue='Dataset', style='Dataset', markers=True, dashes=False)
    
        plt.title(variable + ' over the Years', fontsize=16)
        plt.xlabel('Year', fontsize=14)
        plt.ylabel(variable, fontsize=14)
        plt.legend(title='Dataset', title_fontsize='13', fontsize='11')
        if (variable[0] == '"'):
            variable = variable[1:-1]
    
        plt.savefig('Graphs/' + dir + '/compare_' + variable + '-' + title_base + '-' + title_comparison +'.png', format='png')
        plt.clf()



results_hybrid_logit = getDatasetsHybridLogit()
results_hybrid_cost = getDatasetHybridCost()


for key in results_hybrid_logit:
    compareTripDistributionGraph('Hybrid_Logit',results_hybrid_logit['Business as Usual'], results_hybrid_logit[key], 'Business as Usual', key)
    compareSimpleGraph('Hybrid_Logit',results_hybrid_logit['Business as Usual'], results_hybrid_logit[key], 'Business as Usual', key, 'BUS Daily Occupancy rate')
    compareSimpleGraph('Hybrid_Logit',results_hybrid_logit['Business as Usual'], results_hybrid_logit[key], 'Business as Usual', key, '"Motorization rate number of motorized vehicles per 1000 inhabitants."')


for key in results_hybrid_cost:
    compareTripDistributionGraph('Hybrid_Matrix_Cost',results_hybrid_cost['Business as Usual'], results_hybrid_cost[key], 'Business as Usual', key)

for key in results_hybrid_logit:
    compareTripDistributionGraph('Policy_Testing',results_hybrid_cost[key], results_hybrid_logit[key], 'Cost matrices '+ key, 'LOGIT ' + key)
    compareSimpleGraph('Policy_Testing',results_hybrid_cost[key], results_hybrid_logit[key], 'Cost matrices '+ key, 'LOGIT ' + key, 'BUS Daily Occupancy rate')
