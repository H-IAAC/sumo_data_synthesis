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

    instructions_content = (f"Plan the information of the following student: {student_info}. " + 
                            "Here is the example of the routine of an integral Computer Engineering student: " +
                            "{'time':'7:00'  'location':'home' 'activity':'preparing for classes' />" +
                            "{'time':'8:00'  'location':'FEEC' 'activity':'class' }, " +
                            "{'time':'12:00' 'location':'RA'   'activity':'lunch' }, " +
                            "{'time':'14:00' 'location':'IC'   'activity':'class' }, " +
                            "{'time':'17:00' 'location':'IC'   'activity':'study' }, " +
                            "{'time':'18:00' 'location':'RS'   'activity':'dinner'}, " +
                            "{'time':'20:00' 'location':'home' 'activity':'relax' }, "  
                            )
    message = [
        {
            "role": "system",
            "content": "You have to plan the routine of a student that is going to be between important places inside UNICAMP, you can move between any of " + 
                            "the following places: RU, RA, RS, BC, FEQ, IC, IFGW, IMECC, FEF, FCM, IB, IQ, IB, FCM, FCM, IMECC, IFGW, IC, FEEC. " +
                            "The trip must make sense on the given context. For example, a Chemistry student would spend most of their time " +
                            "at IQ, while a Computer Science student would spend most of their time at IC. " +
                            "Note that RU, RA and RS are restaurants where students go to have breakfast, luch and dinner. " +
                            "Every student must have lunch and dinner at some of the three restaurants. " + 
                            "Students are only having classes from 8:00 to 12:00 or from 14:00 to 18:00. Students DO NOT have classes at 13:00"
                            "Lunch time is from 12:00 to 14:00 and there are no classes and dinner time is from 18:00 to 20:00 and there are no classes. " +
                            "The student must start and end his day at home." + 
                            "Your response should be in the following JSON format. Do not print any other information before or after the schedule:" +
                            '{"time": "current time", "location": "current location", "activity": "current activity"}'
        },
        {
            "role": "user",
            "content": instructions_content,
        }
    ]
    chat_completion = client.chat.completions.create(messages=message, model="llama3-8b-8192", temperature=0.1)

    return chat_completion.choices[0].message.content

student_info = "Chemistry Engineering student. He has most classes at FEQ and has luch at RU and dinner at RA. Today is monday. The student starts and ends his day at home"
print((getResponse_trip(student_info)))