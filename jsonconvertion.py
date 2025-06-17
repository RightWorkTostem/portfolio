import csv
import json

# Replace with your actual CSV file path
csv_file = 'jsonlocation.csv'
output_json_file = 'locations.json'

# List to store the converted data
locations = []

# Read CSV and convert to JSON-like dictionary format
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        lat = float(row['lat'])
        lon = float(row['lon'])
        locations.append([lat, lon])

# Write to a JSON file (with pretty formatting)
with open(output_json_file, 'w') as json_file:
    json.dump(locations, json_file, indent=4)

