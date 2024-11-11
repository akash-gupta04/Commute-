import requests,re

API_KEY = 'API_KEY'

def get_coordinates(address,API_KEY):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'
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


def get_time(start, end, mode,API_KEY):
    start_coords = get_coordinates(start)
    end_coords = get_coordinates(end)
    
    if start_coords and end_coords:
        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start_coords[0]},{start_coords[1]}&destination={end_coords[0]},{end_coords[1]}&mode={mode}&key={API_KEY}'
        response = requests.get(url)
        data = response.json()
        # print(data)
        
        if data['status'] == 'OK':
            # Extracting the distance from the response
            duration = data['routes'][0]['legs'][0]['duration']['text']
            return duration
        else:
            print(f"Error: Could not calculate distance. Status: {data['status']}")
            if 'error_message' in data:
                print(f"Error message: {data['error_message']}")
            return 'Error: Could not calculate distance.'
    else:
        return 'Error: Could not retrieve coordinates for start or end location.'

# Getting distance between two addresses
def get_distance(start, end, mode,API_KEY):

    start_coords = get_coordinates(start)
    end_coords = get_coordinates(end)
    
    if start_coords and end_coords:
        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start_coords[0]},{start_coords[1]}&destination={end_coords[0]},{end_coords[1]}&mode={mode}&key={API_KEY}'
        response = requests.get(url)
        data = response.json()
        # print(data)
        
        if data['status'] == 'OK':
            # Extracting the distance from the response
            distance_with_unit = data['routes'][0]['legs'][0]['distance']['text']
    
            # Use regular expression to extract the numeric part
            distance = float(re.findall(r"[-+]?\d*\.\d+|\d+", distance_with_unit)[0])  # Extracts the numeric value as a float
            
            # Convert to integer
            distance = int(distance)  # Convert the distance to an integer
            return distance
        else:
            print(f"Error: Could not calculate distance. Status: {data['status']}")
            if 'error_message' in data:
                print(f"Error message: {data['error_message']}")
            return 'Error: Could not calculate distance.'
    else:
        return 'Error: Could not retrieve coordinates for start or end location.'




# # Usage example
# start = 'Brampton, Ontario, Canada'
# end = 'Hamilton, Ontario, Canada'

# # Print coordinates and distance
# start_coords = get_coordinates(start)
# end_coords = get_coordinates(end)
# # print(f"Start Coordinates: {start_coords}")
# # print(f"End Coordinates: {end_coords}")

# # Get the walking distance
# # time = get_time(start, end, 'walking')
# # options1 = TransitOptions(start, end,'transit')
# # options = TransitOptions(start, end,'walking')
# # options = TransitOptions(start, end,'bicyling')
# distance = get_distance(start, end, 'walking')
# print(distance)
