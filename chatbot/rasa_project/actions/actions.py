# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from os import getenv
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from pymongo import MongoClient

MONGO_URI = getenv('MONGODB_URI')

def read_data(value):
    assert value in ['temperature1', 'timestamp', 'humidity', 'weight', 'gps']
    client = MongoClient(MONGO_URI)
    db=client.bierbot
    return db.measures.find_one({}, sort=[( '_id', -1)]).get(value)
class ActionOrderDrink(Action):

    def name(self) -> Text:
        return "action_order_drink"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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
                dispatcher.utter_message(f"Kein Getränk ausgewählt.")
            else:
                dispatcher.utter_message(f"{drink_type} ist leider nicht verfügbar.")
            dispatcher.utter_message(response='utter_order_button')

        # elif drink_size not in ['1 Liter', '0.5 Liter']:
        #     if not drink_size:
        #         dispatcher.utter_message(f"Welche Größe?")
        #     else:
        #         dispatcher.utter_message(f"Größe {drink_size} ist leider nicht verfügbar.")
        #     dispatcher.utter_message(buttons = [
        #     {"payload": f'/order\u007b"drink":"{drink_type}","size":"0.5 Liter"\u007d', "title": "0.5 Liter", "button_type": 'vertical'},
        #     {"payload": f'/order\u007b"drink":"{drink_type}","size":"1 Liter"\u007d', "title": "1 Liter", "button_type": 'vertical'}
        #     ])

        else:
            dispatcher.utter_message(text=f"Du hast ein {drink_type} bestellt.")

        return []

class ActionQueryHumidity(Action):

    def name(self) -> Text:
        return "action_query_humidity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        humid = read_data('humidity')

        dispatcher.utter_message(text=f"Die Luftfeuchtigkeit beträgt gerade {humid} Prozent.")

        return []

class ActionQueryTemperature(Action):

    def name(self) -> Text:
        return "action_query_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        temp = read_data('temperature1')

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

        weight = read_data('weight')

        try:
            drink_type = [entity['value'] for entity in tracker.latest_message['entities'] if entity['entity']=='drink'][0]
        except IndexError:
            drink_type = None
        if not drink_type:
            drink_type = 'Getränk'
        
        drink_type = drink_type.capitalize()

        if weight < 100:            
            dispatcher.utter_message(text=f"Dein {drink_type} ist fast leer! Nur noch {weight} Milliliter.")
            dispatcher.utter_message(response='utter_new_order')

        if weight >= 100:
            dispatcher.utter_message(text=f"Du hast noch {weight} Milliliter Bier.")

        print()
        return []