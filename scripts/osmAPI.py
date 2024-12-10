import requests

def geocode_address(address):
    """
    Geocodes an address using the Nominatim API from OpenStreetMap.
    
    Args:
        address (str): The address to geocode.
    
    Returns:
        list: A list of dictionaries with formatted address, latitude, and longitude.
    """
    # URL for the Nominatim API
    url = 'https://nominatim.openstreetmap.org/search'
    
    # Parameters for the API request
    params = {
        'q': address,           # The address to search
        'format': 'json',       # Response format
        'addressdetails': 1     # Include detailed address information
    }

    headers = {
        'User-Agent': 'Student SUMO project (r244808@dac.unicamp.br)'
    }
    
    # Make the request
    response = requests.get(url, params=params, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data:
            # Extract and return formatted address, latitude, and longitude
            results = []
            for result in data:
                results.append({
                    "formatted_address": result['display_name'],
                    "latitude": float(result['lat']),
                    "longitude": float(result['lon'])
                })
            return results
        else:
            return "No results found."
        
    else:
        return f"Error: {response.status_code}"


def find_nearby_building(latitude, longitude, build_type, radius):
    # Overpass API endpoint
    url = "https://overpass-api.de/api/interpreter"
    
    # Overpass API query
    query = f"""
    [out:json];
    (
      node["amenity"="{build_type}"](around:{radius},{latitude},{longitude});
      way["amenity"="{build_type}"](around:{radius},{latitude},{longitude});
      relation["amenity"="{build_type}"](around:{radius},{latitude},{longitude});
      node["shop"="{build_type}"](around:{radius},{latitude},{longitude});
      way["shop"="{build_type}"](around:{radius},{latitude},{longitude});
      relation["shop"="{build_type}"](around:{radius},{latitude},{longitude});
      node["leisure"="{build_type}"](around:{radius},{latitude},{longitude});
      way["leisure"="{build_type}"](around:{radius},{latitude},{longitude});
      relation["leisure"="{build_type}"](around:{radius},{latitude},{longitude});
    );
    out center;
    """
    
    # Make the API request
    response = requests.get(url, params={"data": query})
    
    if response.status_code == 200:
        data = response.json()
        results = []
        
        for element in data.get('elements', []):
            if element['type'] == 'node':
                # Extract coordinates directly for nodes
                lat = element['lat']
                lon = element['lon']
            elif element['type'] in ['way', 'relation']:
                # Use the 'center' key for ways and relations
                center = element.get('center')
                if center:
                    lat = center['lat']
                    lon = center['lon']
                else:
                    # Skip if no center is available
                    continue
            else:
                # Skip unsupported types
                continue
            
            # Add the result
            results.append({
                "name": element.get("tags", {}).get("name", "Unknown"),
                "latitude": lat,
                "longitude": lon,
                "type": element['type']
            })
        return results
    
    else:
        print(f"Error: {response.status_code}")
        return []
    

# Example usage
# latitude = -22.817359  # Latitude of a location (e.g., the White House)
# longitude = -47.071652 # Longitude of a location
# build_type = "general"  # Type of building (e.g., 'school', 'hospital', 'restaurant')
# radius = 1500  # Search radius in meters

# results = find_nearby_building(latitude, longitude, build_type, radius)
# print(results)
