import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# graph comparing all trips through time
# graph comparing two different datasets in terms of co2 emissions
# graph comparing two different datasets in terms of trips
# graph comparing three different datasets in terms of trips

# graph showcasing growth of salaries
#graph with each of the parameters through time 

#funcao que pega num parâmetro e dois saves e faz a comparação dos dois saves em termos desse parâmetro (para tudo o que é SUMP)

def getDatasets():
    results_base = pd.read_csv('Results/results.csv')
    results_bus_lines = pd.read_csv('Results/results_bus_routes.csv')
    results_bus_trips = pd.read_csv('Results/results_bus_trips.csv')
    results_car_increase = pd.read_csv('Results/results_car_increase.csv')
    results_railway_trips = pd.read_csv('Results/results_railway_trips.csv')
    results_railway_routes = pd.read_csv('Results/results_railway_routes.csv')

    datasets = {
    'Business as Usual': results_base[1:],
    'Increase BUS lines': results_bus_lines[1:],
    'Increase BUS trips': results_bus_trips[1:],
    'Increase Road Length': results_car_increase[1:],
    'Increase Railway trips': results_railway_trips[1:],
    'Increase Railway routes': results_railway_routes[1:]
    }   

    return datasets

def cleanResults(results):
    results = results.rename(columns={
        'DAILY CHOSEN CAR': 'Car',
        'DAILY CHOSEN BUS': 'Bus',
        'DAILY CHOSEN RAILWAY': 'Railway',
    }
    )
    return results

def getTripsDistributionGraph(results, title):

    results = cleanResults(results)

    trips_data = results[['Car', 'Bus', 'Railway','time']]

    trips_data = trips_data.reset_index(drop=True).melt(id_vars='time', var_name='Transport', value_name='Daily Chosen')

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=trips_data, x='time', y='Daily Chosen', hue='Transport', marker='o')

    plt.title('Daily Choices of Transport Methods Over Time ' + title, fontsize=16)
    plt.xlabel('Time (years)', fontsize=14)
    plt.ylabel('Number of Trips', fontsize=14)
    plt.legend(title='Transport Method', title_fontsize='13', fontsize='11')

    plt.savefig('Graphs/transport_choices_' + title + '.png', format='png')
    plt.clf()

def getVariableGraph(results, title):
    results = cleanResults(results)
    target_data = results[[title, 'time']]
    sns.lineplot(data=target_data, x='time', y=title)
    plt.title( title + ' over time', fontsize=16)
    plt.xlabel('Time (years)', fontsize=14)
    plt.ylabel(title, fontsize=14)

    plt.savefig('Graphs/' + title + '.png', format='png')
    plt.clf()


     

def compareTripDistributionGraph(results_base, results_comparison, title_base, title_comparison):

    results_base = cleanResults(results_base)
    results_comparison = cleanResults(results_comparison)
    trips_data_base = results_base[['Car', 'Bus', 'Railway','time']]
    trips_data_comparison = results_comparison[['Car', 'Bus', 'Railway','time']]
    
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

    plt.savefig('Graphs/compare_transport_choices_' + title_base + '-' + title_comparison + '.png', format='png')
    plt.clf()


def compareSimpleGraph(results_base, results_comparison, title_base, title_comparison, variable):
    
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
    
        plt.savefig('Graphs/compare_' + variable + '-' + title_base + '-' + title_comparison +'.png', format='png')
        plt.clf()

results = getDatasets()
getTripsDistributionGraph(results['Business as Usual'], 'Business as Usual')
compareTripDistributionGraph(results['Business as Usual'], results['Increase BUS lines'], 'Business as Usual', 'Increase BUS lines')
compareTripDistributionGraph(results['Business as Usual'], results['Increase BUS trips'], 'Business as Usual', 'Increase BUS trips')
compareTripDistributionGraph(results['Business as Usual'], results['Increase Road Length'], 'Business as Usual', 'Increase Road Length')
compareTripDistributionGraph(results['Business as Usual'], results['Increase Railway trips'], 'Business as Usual', 'Increase Railway trips')
compareTripDistributionGraph(results['Business as Usual'], results['Increase Railway routes'], 'Business as Usual', 'Increase Railway routes')


compareTripDistributionGraph(results['Increase BUS trips'], results['Increase BUS lines'], 'Increase BUS trips', 'Increase BUS lines')
compareTripDistributionGraph(results['Increase BUS trips'], results['Increase Railway routes'], 'Increase BUS trips',  'Increase Railway routes')


compareSimpleGraph(results['Business as Usual'], results['Increase BUS lines'], 'Business as Usual', 'Increase BUS lines', 'BUS Daily Occupancy rate')
compareSimpleGraph(results['Business as Usual'], results['Increase BUS trips'], 'Business as Usual', 'Increase BUS trips', 'BUS Daily Occupancy rate')
compareSimpleGraph(results['Business as Usual'], results['Increase Road Length'], 'Business as Usual', 'Increase Road Length', 'BUS Daily Occupancy rate')
compareSimpleGraph(results['Business as Usual'],  results['Increase Railway trips'], 'Business as Usual', 'Increase Railway trips', 'Railway Daily Occupancy rate')
compareSimpleGraph(results['Business as Usual'],  results['Increase Railway routes'], 'Business as Usual', 'Increase Railway routes', 'Railway Daily Occupancy rate')



compareSimpleGraph(results['Business as Usual'], results['Increase BUS lines'], 'Business as Usual', 'Increase BUS lines', '"Motorization rate number of motorized vehicles per 1000 inhabitants."')
compareSimpleGraph(results['Business as Usual'], results['Increase BUS trips'], 'Business as Usual', 'Increase BUS trips', '"Motorization rate number of motorized vehicles per 1000 inhabitants."')
compareSimpleGraph(results['Business as Usual'],  results['Increase Road Length'], 'Business as Usual', 'Increase Road Length', '"Motorization rate number of motorized vehicles per 1000 inhabitants."')
compareSimpleGraph(results['Business as Usual'],  results['Increase Railway trips'], 'Business as Usual', 'Increase Railway trips', '"Motorization rate number of motorized vehicles per 1000 inhabitants."')
compareSimpleGraph(results['Business as Usual'],  results['Increase Railway routes'], 'Business as Usual', 'Increase Railway routes', '"Motorization rate number of motorized vehicles per 1000 inhabitants."')

getVariableGraph(results['Business as Usual'], 'Population')