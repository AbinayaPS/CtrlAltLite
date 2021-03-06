# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import mysql.connector
from app import show_IP

class ActionConfirmType(Action):
    def name(self) -> Text:
        return "action_confirm_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        crime = str(tracker.get_slot("type_of_crime"))
        if crime=="Content related to online sexual abuse":
            dispatcher.utter_message(template="utter_confirm_content_crime")
        else:
            dispatcher.utter_message(template="utter_confirm_other_crime")
        return []

class ActionCustomFallback(Action):
    def name(self) -> Text:
        return "custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("I'm sorry, I didn't get that. Can you try again?")
        return []


class SubCategoryAction(Action):
    def name(self) -> Text:
        return "ask_other_crime_sub_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            other_crime = str(tracker.get_slot("other_crime_type"))
            if other_crime == "loss of money":
                dispatcher.utter_message(template="utter_LOM_sub_category")
            elif other_crime == "online harrassment":
                SlotSet("other_crime_sub_category","Cyber bullying/Stalking/Sexting")
            elif other_crime == "hacking":
                dispatcher.utter_message(template="utter_hacking_sub_category")
            elif other_crime == "hatred and threat":
                dispactcher.utter_message(template="utter_HAT_sub_category")
            elif other_crime == "human trafficking/online prostitution":
                SlotSet("other_crime_sub_category","online trafficking")
            elif other_crime == "online gambling":
                SlotSet("other_crime_sub_category","online gambling")

            return []

class ContentCrimeForm(FormAction):
    def name(self):
        return "content_crime_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("content_crime_confirmation") == "True":
            return ["content_crime_type","platform","link_ID","state_ut","district","date_of_incident","additional_information"]
        else:
            return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "content_crime_type": [
                self.from_entity(entity="content_crime_type"),
            ],
            "platform": [
                self.from_entity(entity="platform"),
            ],
            "link_ID": [
                self.from_text(intent="mention_link"),
            ],
            "state_ut": [
                self.from_entity(entity="state_ut"),
            ],
            "district": [
                self.from_entity(entity="district"),
            ],
            "date_of_incident": [
                self.from_entity(entity="date_of_incident"),
            ],
            "additional_information": [
                self.from_text(intent="mention_information"),
                self.from_text(intent="deny"),
            ],
        }

    #def add_crime_details(details):
        """mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abinaya123",
        database="crimebot"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO crime_reg_details (CrimeType, Platform, Link, State, District, AddInfo) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql,details)
        mydb.commit()"""
    

    def submit(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        # utter submit template
        content_crime_type = str(tracker.get_slot("content_crime_type"))
        platform = str(tracker.get_slot("platform"))
        link = str(tracker.get_slot("link_ID"))
        state_ut = str(tracker.get_slot("state_ut"))
        district = str(tracker.get_slot("district"))
        info = str(tracker.get_slot("additional_information"))
        #ip = show_IP()
        #add_crime_details()
        details = (content_crime_type,platform,link,state_ut,district,info)
        
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abinaya123",
        database="crimebot"
        )
        mycursor = mydb.cursor()
        
        sql = "INSERT INTO crime_reg_details (CrimeType, Platform, Link, State, District, AddInfo) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql,details)
        mydb.commit()
        
        message = "Your report has been taken in. Do not panic!"
        
        dispatcher.utter_message(message)
        return []

class OtherCrimeForm(FormAction):
    def name(self):
        return "other_crime_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("other_crime_confirmation") == "True":
            return ["platform","link_ID","state_ut","district","date_of_incident","additional_information"]
        else:
            return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "platform": [
                self.from_entity(entity="platform"),
            ],
            "link_ID": [
                self.from_text(intent="mention_link"),
            ],
            "state_ut": [
                self.from_entity(entity="state_ut"),
            ],
            "district": [
                self.from_entity(entity="district"),
            ],
            "date_of_incident": [
                self.from_entity(entity="date_of_incident"),
            ],
            "additional_information": [
                self.from_text(intent="mention_information"),
                self.from_text(intent="deny"),
            ],
        }

    #def add_other_details(details):
        """mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abinaya123",
        database="crimebot"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO crime_reg_details (CrimeType, SubCategory, Platform, Link, State, District, AddInfo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql,details)
        mydb.commit()"""

    def submit(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        # utter submit template
        other_crime_type = str(tracker.get_slot("other_crime_type"))
        other_crime_sub_category = str(tracker.get_slot("other_crime_sub_category"))
        platform = str(tracker.get_slot("platform"))
        link = str(tracker.get_slot("link_ID"))
        state_ut = str(tracker.get_slot("state_ut"))
        district = str(tracker.get_slot("district"))
        info = str(tracker.get_slot("additional_information"))
        #ip = show_IP()
        #add_other_details()
        
        details = (other_crime_type,other_crime_sub_category,platform,link,state_ut,district,info)

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abinaya123",
        database="crimebot"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO crime_reg_details (CrimeType, SubCategory, Platform, Link, State, District, AddInfo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql,details)
        mydb.commit()
        
        # message = "Your report: \nType of crime: "+tracker.get_slot("other_crime_type")+ "\n Sub catgory: "+ tracker.get_slot("other_crime_sub_category")+"\n Platform: "+tracker.get_slot("platform")+"\n Link: "+tracker.get_slot("link_ID") + "\n Date: "+tracker.get_slot("date_of_incident")+"\n Information: "+tracker.get_slot("additional_information")
        message = "Your report has been taken in. Do not panic!"
        dispatcher.utter_message(message)
        return []

