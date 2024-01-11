# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from spotify_module import get_token, get_auth_header, search_for_artist

class MyFallback(Action):
    
    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response = "utter_out_of_scope")
        return []

class ActionArtistInfo(Action):
    def name(self) -> Text:
        return "action_artist_info"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artist_name = str(tracker.get_slot('artist'))

        token = get_token()
        artist = search_for_artist(token, artist_name)

        if artist == {}:
            output = f"I don't know anything about {artist_name}. Are you sure you spelled it correctly?"
        else:
            output = (
            f"This is what I know about {artist['name']}:\n"
            f"Genres: {', '.join(artist['genres'])}\n"
            f"Followers: {artist['followers']}\n")
        
        dispatcher.utter_message(text=output, image=artist["image"])
        return []