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