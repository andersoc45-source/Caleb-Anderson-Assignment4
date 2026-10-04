import requests
import json
import csv

def write_csv_file(data_dict):
    """
        Writes city information to city_data.csv.
    
        Args:
            data_dict (dictionary): The data to be sent.
    
        Returns:
            None
    """
    csv_file = "city_data.csv"
    try:
        with open(csv_file, mode='w', newline='') as file:
            fieldnames = data_dict.keys()
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader() # Writes the header row
            csv_writer.writerow(data_dict) # Writes data rows

            print(f"Dictionary data written to '{csv_file}'.")
    except IOError as e:
        print(f"Error writing to file: {e}")

def read_csv_file():
    """
        Prints the number of cities, city name, and temperature.
    
        Args:
            None
    
        Returns:
            None
    """
    csv_file = "city_data.csv"
    cities = []

    try:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                cities.append(row) # Add row to cities list

        # Print data
        print(f"Number of cities: {int((len(cities) + 1) / 2)}")

        for city in cities:
            name = city.get("City")
            temp = city.get("Temperature (C)")
            print(f"{name}: {temp} degrees Celsius")

    except IOError as e:
        print(f"Error reading file: {e}")
    except FileNotFoundError:
        print("Error: city_data.csv not found.")
    except ValueError as e:
        print(f"Error converting data: {e}")


# Retrieve Data from an API
api_key = "096fd8081db6eb4b37e190f9fd2ab2ab"

city_name = input("Enter a city name: ").strip()
while city_name == "": # If city_name is empty, the loop repeats
    city_name = input("Enter a city name: ").strip()

url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"

# Get lat and lon through geocoding request
try:
    response_geocoding = requests.get(url)
    response_geocoding.raise_for_status() # This will raise an HTTPError for 404
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error occurred: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"An unexpected error occurred: {err}")

print(f"Status Code: {response_geocoding.status_code}")
print(f"response_geocoding URL: {response_geocoding.url}")

# Convert JSON data to a Python dictionary
response_geocoding_data = response_geocoding.json()

# Find coordinates
city_coordinates = {
    "lat": response_geocoding_data[0]["lat"],
    "lon": response_geocoding_data[0]["lon"]
}

# Get city data
url = f"https://api.openweathermap.org/data/2.5/weather?lat={city_coordinates["lat"]}&lon={city_coordinates["lon"]}&appid={api_key}"
response_geocoding = requests.get(url)

# Convert to Python
city_data = response_geocoding.json()

city_name = city_data["name"]
city_country = city_data["sys"]["country"]
city_temp_c = (city_data["main"]["temp"] - 273.15) - ((city_data["main"]["temp"] - 273.15) % .001)
city_humidity = city_data["main"]["humidity"]
city_weather = city_data["weather"][0]["description"]

# City data dictionary
city_file_data = {
    "City": city_name,
    "Country": city_country,
    "Temperature (C)": city_temp_c, 
    "Humidity (%)": city_humidity, 
    "Description": city_weather
}

write_csv_file(city_file_data)

read_csv_file()