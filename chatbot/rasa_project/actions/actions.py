# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json

from pymongo import MongoClient

def read_data(value):
    assert value in ['temperature1', 'timestamp', 'humidity', 'weight', 'gps']
    url = 'mongodb+srv://bierbot:@cluster0.q18wv.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(url)
    db=client.bierbot
    return db.measures.find_one().__getattribute__(value)

class ActionOrderDrink(Action):

    def name(self) -> Text:
        return "action_order_drink"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message['sender_id'])
        try:
            drink_type = [entity['value'] for entity in tracker.latest_message['entities'] if entity['entity']=='drink'][0]
        except IndexError:
            print('except IndexError drink_type')
            print(tracker.latest_message['entities'])
            drink_type = None
        try:
            drink_size = [entity['value'] for entity in tracker.latest_message['entities'] if entity['entity']=='size'][0]
        except IndexError:
            print('except IndexError drink_size')
            drink_size = None

        drink_type = drink_type.capitalize()

        if drink_type not in ['Bier', 'Spezi', 'Apfelschorle']:
            if not drink_type:
                dispatcher.utter_message(f"Kein Getränk ausgewählt. Wähle:")
            else:
                dispatcher.utter_message(f"{drink_type} ist leider nicht verfügbar. Wähle:")
            dispatcher.utter_message(buttons = [
            {"payload": '/order{"drink":"Bier"}', "title": "Bier"},
            {"payload": '/order{"drink":"Bier"}', "title": "Spezi"},
            {"payload": '/order{"drink":"Apfelschorle"}', "title": "Apfelschorle"}
            ])

        elif drink_size not in ['1 Liter', '0.5 Liter']:
            if not drink_size:
                dispatcher.utter_message(f"Welche Größe?")
            else:
                dispatcher.utter_message(f"Größe {drink_size} ist leider nicht verfügbar.")
            dispatcher.utter_message(buttons = [
            {"payload": f'/order\u007b"drink":"{drink_type}","size":"0.5 Liter"\u007d', "title": "0.5 Liter"},
            {"payload": f'/order\u007b"drink":"{drink_type}","size":"1 Liter"\u007d', "title": "1 Liter"}
            ])

        else:
            dispatcher.utter_message(text=f"Du hast ein {drink_type} in Größe {drink_size} bestellt.")

        return []

class ActionQueryHumidity(Action):

    def name(self) -> Text:
        return "action_query_humidity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #humid = read_data('humidity')

        dispatcher.utter_message(text=f"Die Luftfeuchtigkeit beträgt gerade {humid} Prozent.")

        return []

class ActionQueryTemperature(Action):

    def name(self) -> Text:
        return "action_query_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #temp = read_data('temperature1')

        if temp > 20:
            dispatcher.utter_message(text=f"Dein Getränk ist zu warm! Schon {temp} Grad. Trink schnell aus!!!")

        if temp <= 20:
            dispatcher.utter_message(text=f"Keine Sorge, dein Getränk hat {temp} Grad.")

        return []

class ActionQueryWeight(Action):

    def name(self) -> Text:
        return "action_query_weight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #weight = read_data('weight')

        try:
            drink_type = [entity['value'] for entity in tracker.latest_message['entities'] if entity['entity']=='drink'][0]
        except IndexError:
            drink_type = None
        if not drink_type:
            drink_type = 'Getränk'
        
        drink_type = drink_type.capitalize()

        if weight < 100:            
            dispatcher.utter_message(text=f"Dein {drink_type} ist fast leer! Nur noch {weight} Milliliter.")
            dispatcher.utter_message(text="Möchtest du ein neues bestellen?")
            dispatcher.utter_message(buttons = [
                    {"payload": f'/order\u007b"drink":"{drink_type}"\u007d', "title": "Ja"},
                    {"payload": "/no_wishes", "title": "Nein"},
                ])

        if weight >= 100:
            dispatcher.utter_message(text=f"Du hast noch {weight} Milliliter Bier.")

        print()
        return []