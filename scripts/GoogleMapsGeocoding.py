import requests
import LLAMAconnect as llama

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

def find_nearby_building(latitude, longitude, build_type, radius, mode='driving'):
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
            if data['results'] == []:
                print(f"No buildings of type {build_type} found nearby")
                return False
            
            for place in data['results']:
                results.append({
                    "name": place['name'],
                    "address": place.get('vicinity', 'No address available'),
                    "latitude": place['geometry']['location']['lat'],
                    "longitude": place['geometry']['location']['lng'],
                    "distance": get_distance(latitude, longitude, place['geometry']['location']['lat'], place['geometry']['location']['lng'], mode)
                })
            return results
        else:
            return False
    else:
        print(f"Error: {response.status_code}")
        return False

def get_distance(origin_lat, origin_lng, dest_lat, dest_lng, mode='driving'):
    # URL for the Distance Matrix API
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    
    # Define the parameters
    params = {
        'origins': f'{origin_lat},{origin_lng}',
        'destinations': f'{dest_lat},{dest_lng}',
        'mode': mode,  # Mode of transportation (driving, walking, bicycling, transit)
        'key': api_key
    }
    
    # Make the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            element = data['rows'][0]['elements'][0]
            if element['status'] == 'OK':
                distance = element['distance']['text']
                duration = element['duration']['text']
                return {
                    'distance': distance,
                    'duration': duration
                }
            else:
                return f"Error: {element['status']}"
        else:
            return f"Error: {data['status']}"
    else:
        return f"Error: {response.status_code}"


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
                    "address_components": result.get('address_components', []),                    "formatted_address": result['formatted_address'],
                    "latitude": result['geometry']['location']['lat'],
                    "longitude": result['geometry']['location']['lng'],
                    "place_id": result.get('place_id', 'No place ID available'),

                })
            return results
        else:
            return f"Error: {data['status']}"
    else:
        return f"Error: {response.status_code}"

def find_nearby_building(latitude, longitude, build_type, radius, mode='driving'):
    # URL for the Places API Nearby Search
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    # Define the parameters
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': f'{build_type}',
        'key': api_key
    }
    
    # Make the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            results = []
            if data['results'] == []:
                print(f"No buildings of type {build_type} found nearby")
                return False
            
            for place in data['results']:
                results.append({
                    "name": place['name'],
                    "address": place.get('vicinity', 'No address available'),
                    "latitude": place['geometry']['location']['lat'],
                    "longitude": place['geometry']['location']['lng'],
                    "place_id": place.get('place_id', 'No place ID available'),
                    "distance": get_distance(latitude, longitude, place['geometry']['location']['lat'], place['geometry']['location']['lng'], mode)
                })
            return results
        else:
            return False
    else:
        print(f"Error: {response.status_code}")
        return False

def get_distance(origin_lat, origin_lng, dest_lat, dest_lng, mode='driving'):
    # URL for the Distance Matrix API
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    
    # Define the parameters
    params = {
        'origins': f'{origin_lat},{origin_lng}',
        'destinations': f'{dest_lat},{dest_lng}',
        'mode': mode,
        'key': api_key
    }
    
    # Make the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            element = data['rows'][0]['elements'][0]
            if element['status'] == 'OK':
                distance = element['distance']['text']
                duration = element['duration']['text']
                return {
                    'distance': distance,
                    'duration': duration
                }
            else:
                return f"Error: {element['status']}"
        else:
            return f"Error: {data['status']}"
    else:
        return f"Error: {response.status_code}"

def get_place_description(place_id):
    """
    Retrieve detailed information about a place, including its description.
    """
    # URL for the Place Details API
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    
    # Define the parameters
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,types,rating,review,user_ratings_total,editorial_summary',
        'key': api_key
    }
    
    # Make the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            result = data['result']
            return {
                "name": result.get('name', 'No name available'),
                "address": result.get('formatted_address', 'No address available'),
                "types": result.get('types', []),
                "rating": result.get('rating', 'No rating available'),
                "user_ratings_total": result.get('user_ratings_total', 'No rating count available'),
                "description": result.get('editorial_summary', {}).get('overview', 'No description available')
            }
        else:
            return f"Error: {data['status']}"
    else:
        return f"Error: {response.status_code}"