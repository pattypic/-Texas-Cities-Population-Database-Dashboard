# File: TCPopulationDash.py
# Date Created: 04/17/23
# Date Last Modified: 01/18/23
# Description of Program:
#
# This Python code is a program that provides census data for cities in Texas, 
# including the population in the 2020 census and estimated population in 2023.

import pandas as pd
import matplotlib.pyplot as plt
 
# This function reads the data from the `citiesData.csv` 
# file and returns a dictionary of city names and population data.

file_path = "citiesData.csv"

# Main functions

def read_city_data(file_path):
    city_data = {}
    city_names = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("#") or line.startswith("City"): 
                    continue
                parts = line.strip().split(",")
                city_name = parts[3].strip('"')
                estimated2023 = int(parts[0])
                census2020 = int(parts[1])
                growth_rate = float(parts[2]) * 100
                city_data[city_name] = (census2020, estimated2023, growth_rate)
                city_names.append(city_name)

    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
        return {}, []

    return city_data, city_names

def calculate_aggregated_data(city_data):
    total_census2020 = sum(x[0] for x in city_data.values())
    total_estimated2023 = sum(x[1] for x in city_data.values())
    total_growth = ((total_estimated2023 - total_census2020) / total_census2020) * 100
    return {"Texas": (total_census2020, total_estimated2023, total_growth)}

def show_growth_data(city_data):
    df = pd.DataFrame.from_dict(city_data, orient='index', columns=['Census 2020', 'Estimated 2023','Growth Rate'])
    
    mean_growth_rate = df['Growth Rate'].mean()
    standard_deviation = df['Growth Rate'].std()
    df['Deviation From Mean'] = (df['Growth Rate'] - mean_growth_rate)
    sorted_df = df.sort_values('Deviation From Mean')
    total_cities_count = len(sorted_df)


    print("\nCities ranked by deviation from average growth rate:\n\n")
    print(f"Growth rate mean {mean_growth_rate:.3f}\t\tGrowth rate standard dev {standard_deviation:.3f}\t\tTotal cities count {total_cities_count:.3f}")
    print(sorted_df)

    plt.figure(figsize=(10, 6))
    plt.hist(df['Growth Rate'], bins=500, color='blue', alpha=0.7)
    
    plt.axvline(mean_growth_rate, color='red', linestyle='dashed', linewidth=2)
    plt.xlabel('Growth Rate (%)')
    plt.ylabel('Frequency')
    plt.title('Histogram of City Growth Rates')
    plt.grid(True)
    plt.show()

    return sorted_df

# This function prints a list of available commands.
def help():
    return print("Enter any of the following commands:\n\033[1mHelp\033[0m - list available commands;\n\033[1mQuit\033[0m - exit this dashboard;\n\033[1mCities\033[0m - list all Texas cities\n\033[1mCensus\033[0m <cityName>/Texas - population in 2020 census by specified city or statewide;\n\033[1mEstimated\033[0m <cityName>/Texas - estimated population in 2023 by specified city or statewide.\n\033[1mGrowth\033[0m <cityName>/Texas - percent change from 2020 to 2023, by city or statewide.\n\033[1mShow Growth Data\033[0m - shows a histograph and data for all growth rates.")


# This function exits the dashboard.
def quit():
    print("\033[1mThank you for using the Texas Cities Population Database Dashboard.  Goodbye!\033[0m")
    exit()


# This function lists all the cities in Texas.
def cities(city_names):
    sorted_names = sorted(city_names)
    print("\n".join(sorted_names))


# This function prints the population of a city in 2020.
def census2020(city_name, city_data, _):
    city_name = city_name.title()
    if city_name == "Texas":
        TXcen2020 = city_data[city_name][0]
        print(f"Total population in Texas in the 2020 Census: {TXcen2020}")
    elif city_name in city_data:
        cen2020 = city_data[city_name][0]
        print(f"{city_name}'s total population in the 2020 Census: {cen2020}")
    else:
        print(f"{city_name} not found in the database.")


# This function prints the estimated population of a city in 2023.
def estimated2023(city_name, city_data, city_names):
    city_name = city_name.title()
    if city_name == "Texas":
        total_estimated = city_data[city_name][1]
        print(f"Total population in Texas in the 2023 Census: {total_estimated}")
    elif city_name in city_data:
        population = city_data[city_name][1]
        if city_name in city_names:
            print(f"{city_name}'s estimated population in 2023:: {population}")
        else:
            print(f"{city_name} is not in Texas")
    else:
        print(f"{city_name} not found in the database.")


# This function prints the percent change from 2020 to 2023, by city or statewide.
def growth(city_name, city_data, city_names):   
    city_name = city_name.title()
    if city_name == "Texas":
        tot_growthrate = city_data[city_name][2]
        print(f"Texas had percent population change from 2020 to 2023: {tot_growthrate:.2f} %")
    elif city_name in city_data:   
        growth_rate = city_data[city_name][2] 
        if city_name in city_names:
            print(f"{city_name}'s percent population change from 2020 to 2023: {growth_rate:.2f} %")
        else:
            print(f"{city_name} is not in Texas")
    else:
        print(f"{city_name} not found in the database.")


# makes for a faster time time complexity then not using a dict here
command_dict = {
    "help": help,
    "quit": quit,
    "cities": cities,
    "census": census2020,
    "estimated": estimated2023,
    "growth": growth,
    "show growth data": show_growth_data
    # "show population data": show_population_data
}

def main():
    # Welcome prompt
    print("\n\033[1mWelcome to the Texas Cities Population Dashboard.\033[0m\nThis provides census data from the 2020 census and\nestimated population data in Texas as of 2023.")
    print("\nCreating dictionary from file: citiesData.csv\n")
    print("Enter any of the following commands:\n\033[1mHelp\033[0m - list available commands;\n\033[1mQuit\033[0m - exit this dashboard;\n\033[1mCities\033[0m - list all Texas cities\n\033[1mCensus\033[0m <cityName>/Texas - population in 2020 census by specified city or statewide;\n\033[1mEstimated\033[0m <cityName>/Texas - estimated population in 2023 by specified city or statewide.\n\033[1mGrowth\033[0m <cityName>/Texas - percent change from 2020 to 2023, by city or statewide.\n\033[1mShow Growth Data\033[0m - shows a histograph and data for all growth rates.")

    city_data, city_names = read_city_data(file_path)

    # loop for the input promts
    while True:
        command = input("\n\033[1mEnter a command:\033[0m ").lower()
        if command in command_dict:
            if command in ["census", "estimated", "growth"]:
                city_data.update(calculate_aggregated_data(city_data))
                input_str = input("\nEnter city name or Texas (e.g. <cityName>/Texas): ")
                command_dict[command](input_str, city_data, city_names)
            elif command == "cities":
                cities(city_names)
            elif command in ["show growth data"]:
                command_dict[command](city_data)
            else:
                command_dict[command]()
        else:
            print('Command not found. Type "Help" for command options.')


if __name__ == "__main__":
    main()