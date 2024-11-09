import requests

API_KEY = 'AIzaSyDT3TNy2KLvYHQWWpJ-IZDjFodhOfDAFeU'

# Geocoding: getting coordinates from address text
def get_coordinates(api_key, address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Error: Could not retrieve coordinates for {address}. Status: {data['status']}")
        if 'error_message' in data:
            print(f"Error message: {data['error_message']}")
        return None

# Getting distance between two addresses
def get_distance(api_key, start, end, mode='walking'):
    start_coords = get_coordinates(api_key, start)
    end_coords = get_coordinates(api_key, end)
    
    if start_coords and end_coords:
        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start_coords[0]},{start_coords[1]}&destination={end_coords[0]},{end_coords[1]}&mode={mode}&key={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'OK':
            # Extracting the distance from the response
            distance = data['routes'][0]['legs'][0]['distance']['text']
            return distance
        else:
            print(f"Error: Could not calculate distance. Status: {data['status']}")
            if 'error_message' in data:
                print(f"Error message: {data['error_message']}")
            return 'Error: Could not calculate distance.'
    else:
        return 'Error: Could not retrieve coordinates for start or end location.'

# Usage example
start = 'Brampton, Ontario, Canada'
end = 'Hamilton, Ontario, Canada'

# Print coordinates and distance
start_coords = get_coordinates(API_KEY, start)
end_coords = get_coordinates(API_KEY, end)
print(f"Start Coordinates: {start_coords}")
print(f"End Coordinates: {end_coords}")

# Get the walking distance
distance = get_distance(API_KEY, start, end, 'walking')
print(f"Distance: {distance}")
