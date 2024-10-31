import requests

# Your API key
api_key = 'AIzaSyDawXekmQroEhqyajmBPqZQv7PpYYARn7c'

def geocode_address(address):
    # URL for the Geocoding API
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    
    # Make the request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            # Extract and return formatted address, latitude, and longitude
            results = []
            for result in data['results']:
                results.append({
                    "formatted_address": result['formatted_address'],
                    "latitude": result['geometry']['location']['lat'],
                    "longitude": result['geometry']['location']['lng']
                })
            return results
        else:
            return f"Error: {data['status']}"
    else:
        return f"Error: {response.status_code}"

import requests

def find_nearby_building(latitude, longitude, build_type, radius):
    # URL for the Places API Nearby Search
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    # Define the parameters
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,  # Search within 1000 meters
        'type': f'{build_type}',  # Type of place to search for
        'key': api_key
    }
    
    # Make the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            results = []
            for place in data['results']:
                results.append({
                    "name": place['name'],
                    "address": place.get('vicinity', 'No address available'),
                    "latitude": place['geometry']['location']['lat'],
                    "longitude": place['geometry']['location']['lng']
                })
            return results
        else:
            return f"Error: {data['status']}"
    else:
        return f"Error: {response.status_code}"


result = geocode_address("IB, Barão Geraldo, Campinas, Brazil")
lat, lon = result[0]['latitude'], result[0]['longitude']
print(lat, lon)
buildings = find_nearby_building(lat, lon, 'restaurant', 500)
print(len(buildings))
for building in buildings:
    print(building['name'], building['address'])