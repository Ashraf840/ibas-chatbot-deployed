# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from multiprocessing import current_process
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from .ticketing.ticketing_api import create_issue_v2


class ActionCreateIssue(Action):
    def name(self) -> Text:
        return "action_create_issue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name_bn = tracker.get_slot('user_name_bn')
        user_name_en = tracker.get_slot('user_name_en')
        user_address = tracker.get_slot('user_address')
        user_email = tracker.get_slot('user_email')
        issue_desc = tracker.get_slot('issue_desc')
        sender_id = tracker.sender_id
        response = create_issue_v2(
            mobile_number="01927040075",
            issuer_name_bn=user_name_bn,
            issuer_name_en=user_name_en,
            address=user_address,
            email=user_email,
            issue_category_oid="ISSUE-OID-0003",
            description=issue_desc,
            issuer_oid="ISSUER-OID-0001",
            sender_id=sender_id
        )
        print(response)
        if response['code'] == 200:
            dispatcher.utter_message(text=f"আপনার সমসস্যাটি আমাদের অবগত করার জন্য ধন্যবাদ, শীঘ্রই আমাদের প্রতিনিধি আপনার সাথে যোগাযোগ করবেন")
        else:
            dispatcher.utter_message(text=f"Error: Ticketing API ISSUE")
            print(user_name_bn)
            print(user_name_en)
            print(user_address)
            print(user_email)
            print(issue_desc)
        return [SlotSet("user_name_bn", None),
                SlotSet("user_name_en", None),
                SlotSet("user_address", None),
                SlotSet("user_email", None),
                SlotSet("issue_desc", None)]


class ValidateBalanceQueryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_issue_creation_form"

    def validate_user_name_bn(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"user_name_bn": slot_value}

    def validate_user_name_en(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"user_name_en": slot_value}

    def validate_user_address(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"user_address": slot_value}

    def validate_user_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"user_email": slot_value}

    def validate_issue_desc(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"issue_desc": slot_value}
