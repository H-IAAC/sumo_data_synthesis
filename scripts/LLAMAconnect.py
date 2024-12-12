import os
import json

from groq import Groq
from tqdm import tqdm

client = Groq(
    api_key = os.getenv("GROQ_API_KEY"),
)


def getResponse(message):
    # Returns a regular LLAMA response
    instructions_content = (f"{message}"
                            )
    message = [
        {
            "role": "user",
            "content": instructions_content,
        }
    ]

    chat_completion = client.chat.completions.create(messages=message, model="llama3-8b-8192")

    return chat_completion.choices[0].message.content

def getResponse_trip(student_info, places):
    # Generate individual responses for the trips

    institute = places['institute']
    university = places['university'][0]
    leisure = places['leisure']
    eating = places['eating']
    shopping = places['shopping']
    sports = places['sports']

    instructions_content = (f"Plan the information of the following student: {student_info}." 
                            )
    message = [
        {
            "role": "system",
            "content": "You needo to plan the routine of a student. I want to know what they do during the day, including having lunch, studying, leisure, shopping and practicing sports. Whenever students are having classes or studying, they MUST be at one of the following places, according to what they are studying which are separated by OR: {institutes}. A biology student would most likely be at the Institute of Biology or at the Institute of Geociences, for example. Whenever students are having lunch, breakfast or dinner, they MUST be at one of the following places: {eating}. Whenever students are having leisure, they MUST be at one of the following places: {leisure}. Whenever students are shopping, they MUST be at one of the following places: {shopping}. Whenever students are praticing sports, they MUST be at the following places: {sports}. Do not use any location that has not been provided. Students have lunch between 12 and 14 and dinner between 18 and 21. Students do not go to any institute after 20. Students only go to the gym once every day. Some days, students go the gas_station. Do not name the places, just choose one of the options. Students spend most of their day having classes at an institute. Your response should be in a JSON format showing only the current location and current activity. Never include locations to activities. Always start the day at time 7 at home and end the day at time 23 at home, update every hour. Locations always have a single place, never two. Follow the example where the first number is the time: {{'7': {{'location':'home', 'activity':'wake up'}}, '8': {{'location':'{institute}', 'activity':'study'}}, '9':{{'location':'cafe', 'activity':'breakfast'}}}}.".format(
                institutes=" or ".join(institute),
                institute=institute[0],
                university=", ".join(university),
                leisure=", ".join(leisure),
                shopping=", ".join(shopping),
                sports=", ".join(sports),
                eating=", ".join(eating)
            )
        },
        {
            "role": "user",
            "content": instructions_content,
        }
    ]
    chat_completion = client.chat.completions.create(messages=message, model="llama3-8b-8192", temperature=1, response_format={"type": "json_object"})

    return chat_completion.choices[0].message.content

def responseCheck(response, total_locations):
    # Checks if the response from the LLM makes sense
    response = json.loads(response)
    if len(response) < 17:
        print("Error: The response is missing some hours")
        return False
    for item in response:
        try:
            local = response[item]['location']
            if local not in total_locations or ',' in local:
                print(f"Error: Invalid location generated '{local}'")
                return False
        except KeyError:
            print("Error: The response is missing a key")
            return False
    return True

def generate_response_trips(student_info, places, number_of_trips=5):
    # Student_info with informations about the student
    # Places with the places that the student can go, it is divided in categories: leisure, eating, shopping, sports, institutes, university

    responses = []
    i = 0
    total_locations = sum(places.values(), []) + ['home']
    with tqdm(total=number_of_trips) as pbar:
        while i < number_of_trips:

            try:
                response = getResponse_trip(student_info, places)

                if responseCheck(response, total_locations):
                    responses.append(response)
                    i += 1
                    pbar.update(1)  # Update the progress bar
                else:
                    print("Invalid response. Generating a new one.")

            except Exception as e:
                print(f"Error generating response {e}. Trying a new one.")

    return responses

def generate_range_parameters(parameters, styles):
    # Generates the range of parameters for the vehicle types. Used in vehParameters.py

    instructions_content = (f"Give the range of values for the following styles: {styles}." 
                            )
    message = [
        {
            "role": "system",
            "content": "You need to return range of values in JSON for parameters that represent how a driver behaves in traffic, give an explanation for why you picked each value. Following, there is a list of parameter, total possible range and description:\n {parameters}.\nThe more aggressive a driver is, the less they tend to cooperate in traffic and the more selfish they are. Do not go beyond the range restriction for the parameters. The response should be generated in the following format: {{'parameter': {{'style': {{'explanation': 'string', 'min': value, 'max': value}}}}}}. For example, if the styles are aggressive and normal: {{'lcCooperative': {{'aggressive': {{'explanation': 'aggresive drivers are not very cooperative', 'min': 0.2, 'max': 0.5}}, 'normal': {{'explanation': 'normal drivers are cooperative', 'min': 0.5, 'max': 0.8}}}}}}.".format(parameters=parameters)
        },
        {
            "role": "user",
            "content": instructions_content,
        }
    ]
    try:
        chat_completion = client.chat.completions.create(messages=message, model="llama3-8b-8192", temperature=0.5, response_format={"type": "json_object"})
    except Exception as e:
        print(f"Error generating response {e}. Trying a new one.")
        return generate_range_parameters(parameters, styles)

    return chat_completion.choices[0].message.content
