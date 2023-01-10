import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY_RF = os.getenv('API_KEY_RF')
API_KEY_FS = os.getenv('API_KEY_FS')


def enrich_fullstory_users(response_list, field_name):
    for survey in response_list:
        print(survey['user_id'])
        response = requests.post(
            f"https://api.fullstory.com/users/v1/individual/{survey['user_id']}/customvars", headers={'Authorization': f'Basic {API_KEY_FS}'}, data=json.dumps({field_name + '_str': survey['selected_response']}))

        print(response, json.dumps(
            {field_name + '_str': survey['selected_response']}))

    print("Data Insertion Complete!")


def extract_refiner_responses(survey_uuid, field_to_extract):

    fullstory_data_list = []

    response = requests.get(
        'https://api.refiner.io/v1/responses?api_key=' + API_KEY_RF + '&form_uuid=' + survey_uuid)

    data = response.json()

    for item in data['items']:
        fullstory_data_list.append({"user_id": item['contact']['remote_id'], "selected_response": item['data']
                                   [field_to_extract]})

    iterations = data['pagination']['last_page']

    if iterations > 1:
        for i in range(1, iterations):
            response = requests.get(
                'https://api.refiner.io/v1/responses?api_key=' + API_KEY_RF + '&form_uuid=' + survey_uuid + "&page=" + i)

            data = response.json()

            for item in data['items']:
                fullstory_data_list.append({"user_id": item})

    return fullstory_data_list


enrich_fullstory_users(extract_refiner_responses(input("Input your survey id: "),
                                                 input("Input the data field: ")), input("Name your user property for Fullstory: "))

# '82e6adb0-45b9-11ed-ab24-c5beb34e9dc4'
# 'hi_there_we_noticed_you_started_registering_for_this_trial_but_didnt_complete_it_wed_love_to_hear_if_you_have_any_feedback_for_us'
# 'refinerTrialsSelectedResponse'
