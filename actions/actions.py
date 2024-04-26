from multiprocessing import current_process
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, SessionStarted, ActionExecuted, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from .ticketing.ticketing_api import (
    # create_issue_v2, 
    get_project_list, 
    get_category_list_by_project_oid, 
    get_user_detail, 
    redirect_to_cso_chatroom
    )
from .ticketing.ticketing_api import reqres,category_oid, issue_text

import sys
sys.path.append("/media/robin/Documents/PersonalWorks/ibas_project")
from lang_detection.text_lang_detect import lang_detect
from gibberish_identification.gibberish_detection import is_gibberish

import requests, json
import pandas as pd
class ActionCreateIssue(Action):
    def name(self) -> Text:
        return "action_create_issue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text_language = None
        events = tracker.events
        user_events = [e for e in events if e.get('event') == 'user']
        if len(user_events) < 2:
            return []
        elif len(user_events) == 3:
            previous_message = user_events[-2].get('text')
            issue_desc = previous_message
            print("issue", issue_desc)
        else:
            previous_message = user_events[-2].get('text')
            issue_desc = previous_message
            print("issue", issue_desc)

        sender_id = tracker.sender_id

        my_slot_value = tracker.latest_message.get("text")
        category_oid = my_slot_value[8:]
        category = my_slot_value[20:]
        print("category oid issue creation:", category_oid)

        print("The value of the slot is:", my_slot_value)
        print("The value of the trimmed slot is:", my_slot_value[21:])

        print("Check if the user is authenticated! Sned the 'sender_id' to the API")

        # Despite being logged in the system, the user is using the chatbot from the login page checking code block
        response = requests.post(
            'http://127.0.0.1:8080/auth/user-auth/api/is-authenticated/', json.dumps({"senderId": sender_id}),
            headers= {'Content-Type': 'application/json'}
        )
        # print("User is-authenticated api called result: ", response.json())

        user_auth_data = response.json()
        print("User authenticated:", user_auth_data['is_authenticated'])
        print("User authenticated (Type):", type(user_auth_data['is_authenticated']))

        text_language = lang_detect(issue_desc)
        
        if not user_auth_data['is_authenticated']:
            print("Please login first!")

            if text_language == 'bn':
                dispatcher.utter_message(text=f"দয়া করে প্রথমে লগ ইন করুন।")
            else :
                dispatcher.utter_message(text=f"Please login first.")
            return []
        else:
            # If an authenticated user after logging into the system comes back to the login page & start using the chatbot.
            # print("TMS Issue & chatroom create API!")

            # Fetch user detail from from the api & use an old static issue (without creating any issue to TMS), call the chatroom create API.
            print("Fetch an old unresolved issue from TMS!")
            # response = fetch_tms_issue()
            # print("Old Issue detail:", response)
            
            response = requests.get(f'http://127.0.0.1:8080/home/api/user-chatbot/socket/{sender_id}/')
            data = response.json()

            # Add the new fallback message of chatbot to 'Augmented Data Sentence excel file'
            new_update_dataset = '/media/robin/Documents/PersonalWorks/ibas_project/source/aug_data_sen.xlsx'
            existing_df = pd.read_excel(new_update_dataset, sheet_name='Sheet1', engine='openpyxl')

            updated_df = pd.concat([existing_df, pd.DataFrame({'Augmented_text': [issue_desc]})],ignore_index=True)

            updated_df.to_excel(new_update_dataset, index=False, engine='openpyxl')

            if text_language == 'bn':
                dispatcher.utter_message(text=f"আপনার সমস্যা সম্পর্কে আমাদের অবহিত করার জন্য আপনাকে ধন্যবাদ। শীঘ্রই একজন হেল্প ডেস্ক অফিসার আপনার সাথে যোগাযোগ করবে।")
            else :
                dispatcher.utter_message(text=f"Thank you for informing us about your issue. A help desk officer will contact you shortly")
            ################ hit api to redirect to the chatroom###################
            url = "http://127.0.0.1:8080/home/api/user-chatroom/socket/"

            payload = json.dumps({
                "user_email": f"{data['user_email']}",
                "chatbot_socket_id": f"{sender_id}",
                "issuerOid": "03209c1c-aef4-46a2-9a9e-418575467be1",

                "user_organization": f"{data['user_organization']}",
                "location": f"{data['location']}",
                "district": f"{data['district']}",
                "division": f"{data['division']}",
                "prompt_user": "True",
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.post(
                url, payload,
                headers= headers
            )

            return []

        


#         # Going to be shifted in webEnd (Currently may be not) ------------------------------------
# 	    ################ NEW #################
#         project_oid = "14f7bcb8-5cf2-47c4-8e4d-a14cf7edbff6"
#         list = get_category_list_by_project_oid(project_oid)
#         print(list)
#         for project_data in list['data']:
#             print(project_data['category_title_bn'], project_data['category_title_en'],category)
#             if project_data['category_title_bn'] == category or project_data['category_title_en']==category:
#                 category_oid = project_data['oid']
#                 print("oid:", category_oid)
#             else:
#                 print("Nothing matched")
#         #################################

#         response = requests.get(f'http://127.0.0.1:8080/home/api/user-chatbot/socket/{sender_id}/')
#         data = response.json()

#         print("Data:   ",data)
#         response = create_issue_v2(
#             mobile_number = data['phone'],
#             issuer_name_bn = data['user_name_bn'],
#             issuer_name_en = data['first_name'],
#             address = data['user_address'],
#             email = data['user_email'],
#             issue_category_oid = category_oid,
#             description = issue_desc,
#             issuer_oid = None,
#             sender_id = sender_id
#         )
#         text_language = lang_detect(issue_desc)

#         if response['code'] == 200:
#             print("Code is reaching here")

#             new_update_dataset = '/home/robin/Downloads/iba_chat_system_tada_module_collaborated_branch/new/source/aug_data_sen.xlsx'
#             existing_df = pd.read_excel(new_update_dataset, sheet_name='Sheet1', engine='openpyxl')

#             updated_df = pd.concat([existing_df, pd.DataFrame({'Augmented_text': [issue_desc]})],ignore_index=True)

#             updated_df.to_excel(new_update_dataset, index=False, engine='openpyxl')

#             if text_language == 'bn':
#                 dispatcher.utter_message(text=f"আপনার সমস্যা সম্পর্কে আমাদের অবহিত করার জন্য আপনাকে ধন্যবাদ।")
#             else :
#                 dispatcher.utter_message(text=f"Thank you for informing us about your issue.")
#             ################ hit api to redirect to the chatroom###################
#             url = "http://127.0.0.1:8080/home/api/user-chatroom/socket/"

#             payload = json.dumps({
#                 "user_email": f"{data['user_email']}",
#                 "chatbot_socket_id": f"{sender_id}",
#                 "issuerOid": f"{response['data']}",

#                 "user_organization": f"{data['user_organization']}",
#                 "location": f"{data['location']}",
#                 "district": f"{data['district']}",
#                 "division": f"{data['division']}",
#                 "prompt_user": "True",
#             })
#             headers = {
#             'Content-Type': 'application/json'
#             }

#             response = requests.post(
#                 url, payload,
#                 headers= headers
#             )

#             message = response.content.decode("utf-8")
#             json_message = json.loads(message)


#             if json_message == {"message": "CSO is avaiable! No msg was created yet!"}:
#                 pass
#             else:
#                 if text_language == 'bn':
#                     dispatcher.utter_message("আপনার সমস্যা রেকর্ড করা হয়েছে। আমরা শীঘ্রই সমস্যা সম্পর্কে আপনার সাথে যোগাযোগ করব।")
#                 else :
#                     dispatcher.utter_message("Your issue has been recorded. We will shortly contact to you about the problem.")
#  ########################################################
#         else:
#             if text_language == 'bn':
#                 dispatcher.utter_message("দুঃখিত কোনো ধরনের সমস্যা হয়েছে, পুনরায় চেষ্টা করুন।")
#             else: 
#                 dispatcher.utter_message("Sorry something went wrong, please try again.")
#         # Going to be shifted in webEnd (Currently may be not) ------------------------------------
        


        text_language = lang_detect(issue_desc)
        if text_language == 'bn':
            dispatcher.utter_message(text=f"আপনার সমস্যা সম্পর্কে আমাদের অবহিত করার জন্য আপনাকে ধন্যবাদ।")
        else :
            dispatcher.utter_message(text=f"Thank you for informing us about your issue.")

        print("sender_ID:",sender_id)

        print("Action create issue was called")
        return []

class ActionProjectCategory(Action):

    def name(self) -> Text:
        return "action_show_project_category"

    def run(self, dispatcher, tracker, domain):
        buttons = []

        return []

class ActionGetProjectOID(Action):
    def name(self) -> Text:
        return "action_get_project_oid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project_oid= tracker.latest_message.get("text")
        SlotSet("issue_description", project_oid)
        print("project_oid:", project_oid)
        issue_text(project_oid)

        return []


class ActionGetCategory(Action):
    def name(self) -> str:
        return "action_get_category_oid"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        category_oid= tracker.latest_message.get("text")
        return []

class ActionSetCategory(Action):
    def name(self) -> str:
        return "action_set_category_oid"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        category_oid= tracker.latest_message.get("text")
        SlotSet("category", category_oid)
        return []

class ActionShowCategoryList(Action):
    def name(self) -> str:
        return "action_show_category_list"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        last_msg = tracker.latest_message.get("text")
        # Check if the last message is gibberish
        if is_gibberish(last_msg):
            if lang_detect(last_msg)== 'bn':
                dispatcher.utter_message("দুঃখিত ! অনুগ্রহ করে সঠিক তথ্য দিয়ে পুনরায় আবার চেষ্টা করুন।")
            else:
                dispatcher.utter_message("Sorry! Please try again with correct information.")
            return []

        buttons = []
        project_oid = "14f7bcb8-5cf2-47c4-8e4d-a14cf7edbff6"    # Static value; manually create project in TMS, get the value from the URL & set that here
        list = get_category_list_by_project_oid(project_oid)

        if lang_detect(last_msg)== 'bn':
            for project_data in list['data']:
                buttons.append({
                "title": project_data['category_title_bn'],
                "payload": 'category' + project_data['oid']
                })
            #dispatcher.utter_message("দুঃখিত, আপনার সমস্যাটি এই মুহুর্তে সমাধান করা সম্ভব হচ্ছে না, আমাদের প্রতিনিধি খুব শীঘ্রই বিষয়টি নিয়ে আপ্নার সাথে যোগাযোগ করবেন")
            
            # dispatcher.utter_message("দুঃখিত, আমরা বর্তমানে আপনার প্রশ্নের উত্তর দিতে পারছি না। <br>আপনার সমস্যাটির শ্রেণী নির্বাচন করুনঃ ", buttons = buttons)
            dispatcher.utter_message("দুঃখিত, আমি বর্তমানে আপনার প্রশ্নের উত্তর দিতে পারছি না। আপনি কি একজন HDO এর সংযোগ করতে চান?", buttons = buttons)
       
        else:
            for project_data in list['data']:
                buttons.append({
                "title": project_data['category_title_en'],
                "payload": 'category' + project_data['oid']
                })
            #dispatcher.utter_message("Sorry, your issue cannot be resolved at this time, our representative will contact you shortly")
            
            # dispatcher.utter_message("Apologies, we are currently unable to provide a response to your query. <br>Please select the category of your issue: ", buttons = buttons)
            dispatcher.utter_message("Apologies, I am currently unable to respond to your query. <br>Do you want to connect your HDO?", buttons = buttons)

        return []

class ActionRedirectWebsite(Action):
    def name(self) -> Text:
        return "action_redirect_website"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []


class ActionCheckNid(Action):
    def name(self) -> Text:
        return "action_check_nid"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []

