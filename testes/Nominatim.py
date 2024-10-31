import requests

# Define the URL with the query
url = "https://nominatim.openstreetmap.org/search"

def getResponse(location, format='json'):
    params = {
        'q': f'{location}',
        'format': f'{format}'
    }
    headers = {
    'User-Agent': 'StudentExperiment/1.0 r244808@dac.unicamp.br'
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        places = response.json()
        if len(places) == 0:
            print("No results found.")
            return
        for place in places:
            print("Name:", place.get("display_name"))
            print("Latitude:", place.get("lat"))
            print("Longitude:", place.get("lon"))
            print("Type:", place.get("type"))
            print()
    else:
        print("Error:", response.status_code)

getResponse("Instituto de Biologia, Campinas, Brazil")