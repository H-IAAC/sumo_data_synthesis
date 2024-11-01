import os
import json

from groq import Groq
from tqdm import tqdm

os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key = os.environ.get("GROQ_API_KEY"),
)

def getResponse_trip_unicamp(student_info):

    instructions_content = (f"Plan the information of the following student: {student_info}. Students do not have classes during lunch and dinner time" 
                            )
    message = [
        {
            "role": "system",
            "content": "You have to plan the routine of multiple students that are going to be between important places inside UNICAMP, you can move them between any of " + 
                            "the following places: HOME, RU, RA, RS, BC, FEQ, IC, IFGW, IMECC, FEF, IB, IQ, IG, IB, IMECC, IFGW, IC, FEEC. FEE does not exist. " +
                            "The trip must make sense on the given context. For example, a Chemistry student would spend most of their time. " +
                            "at IQ, while a Computer Science student would spend most of their time at IC. " +
                            "Chemistry students spend most of ther time at IQ and IB." +
                            "Computer Science students spend most of their time at IC." +
                            "Physics students spend most of their time at IFGW." +
                            "Math students spend most of their time at IMECC." +
                            "Physical Education students spend most of their time at FEF." +
                            "Geography and Geology students spend most of their time at IG." +
                            "Biology students spend most of their time at IB." +
                            "Computer Engineering students spend most of their time at FEEC." +
                            "RU, RA and RS are restaurants where students go to have breakfast, luch and dinner, or they can decide to go home. " +
                            "Every student must have lunch and dinner at some of the three restaurants and they take at most 1 hour eat. " +
                            "Students can only have lunch and dinner once per day." +
                            "Students do not study, spend their free time or relax at RU, RA and RS. " +
                            "Students pratice sports at FEF. " +
                            "Students go to BC or to any other institute to study during their free time. " +
                            "Students are only having classes from 8 to 12 or from 14 to 18. Students DO NOT have classes at 13." +
                            "A few students do not have all the classes, so they can have free time during the day." +
                            "All the engineering students have classes all day long." +
                            "Do not do the same trip for all students, they have different routines." +
                            "Lunch time is from 12 to 14 and there are no classes and dinner time is from 18 to 20 and there are no classes. " +
                            "The student must start and end his day at home. You must create an entry for every 1 hour. The time format is 'hour'" + 
                            "Each student is defined by a trip. Your response should be in a JSON format showing the current location and current activity, always start at time 7. Follow the example: " +
                            "'trip1': {7': {'location':'HOME', 'activity':'wake up' }, 'trip2': {'8': {'location':'HOME', 'activity':'breakfast' } }" 
        },
        {
            "role": "user",
            "content": instructions_content,
        }
    ]
    chat_completion = client.chat.completions.create(messages=message, model="llama3-8b-8192", temperature=0.4, response_format={"type": "json_object"})

    return chat_completion.choices[0].message.content

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
            "content": "You needo to plan the routine of a student. I want to know what they do during the day, including having lunch, studying, leisure, shopping and practicing sports. Whenever students are having classes or studying, they MUST be at one of the following places, which are separated by OR: {institutes}. Whenever students are having lunch, breakfast or dinner, they MUST be at one of the following places: {eating}. Whenever students are having leisure, they MUST be at one of the following places: {leisure}. Whenever students are shopping, they MUST be at one of the following places: {shopping}. Whenever students are praticing sports, they MUST be at the following places: {sports}. Do not use any location that has not been provided. Students have lunch between 12 and 14 and dinner between 18 and 21. Students do not go to {institute} after 20. Students only go to the gym once every day. Some days, students go the gas_station. Do not name the places, just choose one of the options. Students spend most of their day at {institute}. Your response should be in a JSON format showing only the current location and current activity. Never include locations to activities. Always start the day at time 7 at home and end the day at time 23 at home, update every hour. Locations always have a single place, never two. Follow the example where the first number is the time: {{'7': {{'location':'home', 'activity':'wake up'}}, '8': {{'location':'{institute}', 'activity':'study'}}, '9':{{'location':'cafe', 'activity':'breakfast'}}}}.".format(
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