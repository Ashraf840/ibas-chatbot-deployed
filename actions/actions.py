from multiprocessing import current_process
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, SessionStarted, ActionExecuted, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from .ticketing.ticketing_api import create_issue_v2, get_project_list, get_category_list_by_project_oid, get_user_detail, redirect_to_cso_chatroom
from .ticketing.ticketing_api import reqres,category_oid, issue_text
import requests, json
class ActionCreateIssue(Action):
    def name(self) -> Text:
        return "action_create_issue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # issue description detection
        events = tracker.events
        user_events = [e for e in events if e.get('event') == 'user']
        print(" user events" ,len(user_events))
        if len(user_events) < 2:
            print("happenig <2")
            return []
        elif len(user_events) == 3:
            previous_message = user_events[-2].get('text')
            issue_desc = previous_message
            print("issue", issue_desc)
            print("happenig <3")
        else: 
            previous_message = user_events[-2].get('text')
            issue_desc = previous_message
            print("issue", issue_desc)
            print("happenig <4")
       
        #Track sender id which is the socket id
        sender_id = tracker.sender_id

        my_slot_value = tracker.latest_message.get("text")
        category_oid = my_slot_value[8:]
        print("category oid issue creation:", category_oid)

        # Print the value of the slot
        print("The value of the slot is:", my_slot_value)
        print("The value of the trimmed slot is:", my_slot_value[8:])

        # Get User detail of the loggedin user from IBAS 
        response = requests.get(f'http://127.0.0.1:8080/home/api/user-chatbot/socket/{sender_id}/')
        data = response.json()
        # return data

        # data = get_user_detail()
        print("data:  ", data)

        # Create issue and get response
        response = create_issue_v2(
            mobile_number = data['phone'],
            issuer_name_bn = data['user_name_bn'],
            issuer_name_en = data['first_name'],
            address = data['user_address'],
            email = data['user_email'],
            issue_category_oid = category_oid,
            description = issue_desc,
            issuer_oid = None,
            sender_id = sender_id
        )
        print("response",response)

        # If the connection is successful then redirect to the chatroom and connect with the chat operator
        if response['code'] == 200:
            dispatcher.utter_message(
                text=f"আপনার সমসস্যাটি আমাদের অবগত করার জন্য ধন্যবাদ, শীঘ্রই আমাদের প্রতিনিধি আপনার সাথে যোগাযোগ করবেন")
            # message = "[click here](https://www.facebook.com)"
            # dispatcher.utter_message(text=message)
            ################ hit api to redirect to the chatroom###################
            
            url = "http://127.0.0.1:8080/home/api/user-chatroom/socket/"

            payload = json.dumps({
            "user_email": f"{data['user_email']}",
            "chatbot_socket_id": f"{sender_id}",
            "issuerOid": f"{response['data']}"
            })
            headers = {
            'Content-Type': 'application/json'
            }
            
            # response = requests.request("POST", url, headers=headers, data=payload)
            response = requests.post(
                "http://127.0.0.1:8080/home/api/user-chatroom/socket/", payload,
                headers= headers
            )
            print("response 2", response)
            message = response.content
            cso_available = b'"CSO is avaiable! No msg was created yet!"'

            if message == cso_available:
                pass
            else:
                dispatcher.utter_message(text=message)
            ########################################################
        else:
            dispatcher.utter_message(text=f"Error: Ticketing API ISSUE")
            print(data['user_name_bn'])
            print(data['user_name_en'])
            print(data['user_address'])
            print(data['user_email'])
            print(issue_desc)


        dispatcher.utter_message(
                text=f"আপনার সমসস্যাটি আমাদের অবগত করার জন্য ধন্যবাদ, শীঘ্রই আমাদের প্রতিনিধি আপনার সাথে যোগাযোগ করবেন")
        print("sender_ID:",sender_id)

        print("Action create issue was called")
        return []

class ActionProjectCategory(Action):

    def name(self) -> Text:
        return "action_show_project_category"

    def run(self, dispatcher, tracker, domain):
        buttons = []
        # list = get_project_list()

        # # Show button of the project category
        # for project_data in list['data']:
        #     buttons.append({
        #       "title": project_data['project_title_bn'],
        #       "payload": project_data['oid']
        #     })

        # dispatcher.utter_message("project id:  ", buttons = buttons)
        print("action project category was called")

        return []

class ActionGetProjectOID(Action):
    def name(self) -> Text:
        return "action_get_project_oid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # payload = tracker.latest_message.get("payload")
        # print("payload: ", payload)
        project_oid= tracker.latest_message.get("text")
        SlotSet("issue_description", project_oid)
        print("project_oid:", project_oid)
        issue_text(project_oid)
        # if payload :
        #     response = ActionCreateIssue().run(dispatcher, tracker, domain)
        #     print(response)
        #     dispatcher.utter_message("good")
        # else :
        #     pass

        print('action get project oid called')

        return []


class ActionGetCategory(Action):
    def name(self) -> str:
        return "action_get_category_oid"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        #test purpose class
        category_oid= tracker.latest_message.get("text")
        print("Project list Oid:", category_oid)
        print("action get category oid was called")
        return []

class ActionSetCategory(Action):
    def name(self) -> str:
        return "action_set_category_oid"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        #test purpose class
        category_oid= tracker.latest_message.get("text")
        SlotSet("category", category_oid)
        print("Category Oid 2:", category_oid)
        print("action set category oid was called")
        return []

class ActionShowCategoryList(Action):
    def name(self) -> str:
        return "action_show_category_list"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        project_oid = tracker.latest_message.get("text")
        buttons = []
        project_oid = "16321052-ad11-4d4d-a8ec-4f6c0aeed310"
        list = get_category_list_by_project_oid(project_oid)
        for project_data in list['data']:
            buttons.append({
              "title": project_data['category_title_bn'],
              "payload": 'category' + project_data['oid']
            })

        dispatcher.utter_message("আপনার সমস্যাটির শ্রেণী নির্বাচন করুনঃ ", buttons = buttons)
        print("action_show_category_list")
        category_oid = tracker.latest_message.get("text")
        print("category oid", category_oid)

        return []

class ActionRedirectWebsite(Action):
    def name(self) -> Text:
        return "action_redirect_website"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        # # set the URL of the website to redirect to
        # website_url = "https://www.example.com"
        
        # # create a WebexteButton attachment with the website URL
        # button = {"title": "Click here to visit the website", "url": website_url, "webexte": True}
        
        # # send a message with the button attachment
        # dispatcher.utter_message(text="Redirecting to the website...", buttons=[button])

        return []

# class ActionCheckNid(Action):
#     def name(self) -> Text:
#         return "action_check_nid"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         nid = tracker.get_slot("user_nid")
#         print(nid)
#             # data = get_user_detail()
#             # actual_nid = data['user_NID_no']

#             # while True:
#             #     # retrieve user input from the slot
#             #     user_nid = tracker.get_slot("user_nid")
                
#             #     # check if user input matches the actual nid
#             #     if user_nid == actual_nid:
#             #         dispatcher.utter_message("NID verified successfully.")
#             #         break  # exit the loop if the user input is correct
#             #     else:
#             #         # dispatcher.utter_message("Invalid NID. Please try again.")
#             #         user_nid = input("Invalid NID. Please enter your NID: ")
#             #         # reset the slot value to None to prompt the user for input again
#             #         return [SlotSet("user_nid", user_nid)]
            
#             # dispatcher.utter_message(intent="nid_validation_confirmation")
#             # dispatcher.utter_message("utter_nid", tracker)
#         # Validate NID against Django project database
#         # If NID is valid, return a message with a link to the customer support chatroom
#         # If NID is invalid, return a message asking the user to try again
#         return []

class ActionCheckNid(Action):
    def name(self) -> Text:
        return "action_check_nid"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nid = tracker.get_slot("user_nid")
        print(nid)
        # Code to check if the user's NID is valid
        # ...
        data = get_user_detail()
        actual_nid = data['user_NID_no']
        print(actual_nid)
        while True:
            # retrieve user input from the slot
            user_nid = tracker.get_slot("user_nid")
            
            # check if user input matches the actual nid
            if user_nid == actual_nid:
                dispatcher.utter_message("NID verified successfully.")
                break  # exit the loop if the user input is correct
            # elif user_nid == None:
            #     dispatcher.utter_message("")
            else:
                # dispatcher.utter_message("Invalid NID. Please try again.")
                dispatcher.utter_message(text="Invalid NID. Please enter your NID:")
                ActionExecuted('action_listen')
                # reset the slot value to None to prompt the user for input again
                return [SlotSet("user_nid", None)]
        # # If the NID is valid, show the project category buttons
        # if nid:
        #     # Get the list of projects
        #     project_list = get_project_list()
        #     # Create a list of button objects
        #     buttons = []
        #     for project_data in project_list['data']:
        #         button = {
        #             "title": project_data['project_title_bn'],
        #             "payload": project_data['oid']
        #         }
        #         buttons.append(button)
        #     # Use the dispatcher.utter_message() method to send a message to the user interface that includes the buttons
        #     dispatcher.utter_message(text="আপনার সমস্যাটির শ্রেণী নির্বাচন করুনঃ", buttons=buttons)
        # # If the NID is invalid, prompt the user to try again
        # else:
        #     dispatcher.utter_message("Invalid NID. Please try again.")

        return []