# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from multiprocessing import current_process
# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker, FormValidationAction
# from rasa_sdk.events import SlotSet
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.types import DomainDict

# from .dao import DatabaseQuery


# class ActionTellBalance(Action):
#     def name(self) -> Text:
#         return "action_tell_balance"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         current_account_no = next(tracker.get_latest_entity_values('account_no'), None)
#         db_query = DatabaseQuery('./sqlitedb/chatbotdb')
#         balance = db_query.get_account_balance(current_account_no)
#         if balance:
#             dispatcher.utter_message(text=f"আপনার একাউন্টে বর্তমানে {balance} টাকা আছে। ধন্যবাদ।")
#             return [SlotSet("account_no", None)]
#         else:
#             dispatcher.utter_message(text=f"দুঃখিত! আমরা একাউন্টটি খুঁজে পাই নি। "
#                                           f"দয়া করে আপনার একাউন্ট নম্বর {current_account_no} চেক করুন এবং আবার চেষ্টা করুন।  ধন্যবাদ।")
#             return [SlotSet("account_no", None)]


# class ValidateBalanceQueryForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_balance_query_form"

#     def validate_account_no(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate `account_no` value."""

#         if not slot_value.isdecimal():
#             dispatcher.utter_message(text=f"অ্যাকাউন্ট নম্বরে শুধুমাত্র সংখ্যা থাকতে হবে.")
#             return {"account_no": None}
#         dispatcher.utter_message(text=f"ঠিক আছে! আপনার অ্যাকাউন্ট নম্বর হল {slot_value}.")
#         return {"account_no": slot_value}

# class ActionAskAccountNumber(Action):
#     def name(self) -> Text:
#         return "action_ask_account_number"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="অনুগ্রহ করে আপনার অ্যাকাউন্ট নম্বরটি লিখুন।")
#         return []
#
#

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
