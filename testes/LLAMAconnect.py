import os
from groq import Groq
import json
os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key = os.environ.get("GROQ_API_KEY"),
)

def getResponse_xml(path, veh_id, departure_time, parking_area_duration):
    path_str = ""
    path = ["FEEC", "pa75701374#0", "FEEC"]
    path_str += f"from='{path[0]}'"
    for i in range(1, len(path)):
        if i == len(path) - 1:
            path_str += f" to='{path[i]}'"
        else:
            path_str += f", {path[i]},"

    instructions_content = ("Be concise, show only the code. " + 
                    "Given the following trip example: <trip id='veh_id' type='veh_passenger' depart='21.89' departLane='best' from='begin_id' to='end_id'> <stop parkingArea='parkingArea_id' duration='200' /> </trip>. "
                    f'Give me a trip that follows the ids {path_str}.' +
                    "The from parameter of the trip is the first edge, the to paremeter is the last edge. " +
                    f"The depart is going to be at {departure_time}. " +
                    f"The veh_id is going to be {veh_id}. " +
                    "A stop is going to be created for each edge that starts with 'pa'. " +
                    f"The duration of the stop is {parking_area_duration}. " +
                    "Create a trip that is in the same format as the example trip."
                    "Aswer me using a JSON. "
                    )
    message = [
        {
            "role": "user",
            "content": instructions_content,
        }
    ]

    chat_completion = client.chat.completions.create(messages=message, model="llama3-8b-8192", temperature=0.0)

    return chat_completion.choices[0].message.content

def getResponse_trip(student_info):

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

# student_info = "A Computer Engineering student and a Computer Science student. They usually have lunch together at RU. The students are never late to classes."
# print(getResponse_trip(student_info))

def getResponse_coordinates(location):
    instructions_content = (f"Give me the coordinates of the following location at UNICAMP: {location}"
                            )
    message = [
        {
            "role": "system",
            "content": "You need to give me coordinates for given buildings inside the State University of Campinas at Cidade Universitária - Campinas. " +
                        "Always answer using a JSON contaning 'latitude, longitude' and nothing more." +
                        "Be as precise as possible. The building is located inside the campus.",
        },
        {
            "role": "user",
            "content": instructions_content,
        }
    ]

    chat_completion = client.chat.completions.create(messages=message, model="llama3-8b-8192", temperature=0.0, response_format={"type": "json_object"})

    return chat_completion.choices[0].message.content

def getResponse(message):

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


# THIS RESPONSE IS NOT WORKING PROPERLY
# response = getResponse_coordinates("Faculdade de Engenharia Elétrica e de Computação da Universidade Estadual de Campinas - FEEC/UNICAMP")
# print(json.loads(response)['latitude'], ",", json.loads(response)['longitude'])

response = getResponse("Give me the name of all institute and schools at Unicamp, Brazil. Be sucint, give only the name.")
print(response)