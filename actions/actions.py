from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from spotify_module import get_similar_artists, get_songs_by_artist, get_token, get_auth_header, search_for_artist, milliseconds_to_string, get_albums_by_artist

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

        if artist_name == "None" or artist_name == "":
            dispatcher.utter_message(text="You haven't provided an artist name.")
            return [SlotSet("artist", None)]

        token = get_token()

        artist = search_for_artist(token, artist_name)

        if artist == None:    
            output = f"I don't know anything about {artist_name}. Are you sure you spelled it correctly?"
            dispatcher.utter_message(text=output)
            return [SlotSet("artist", None)]
        else:
            output = (
                    f"This is what I know about {artist['name'].upper()}:\n"
                    f"• genres: {', '.join(artist['genres'])}\n"
                    f"• followers: {artist['followers']}\n"
                ) 
            dispatcher.utter_message(text=output, image=artist["image"])
            return []
        
class ActionTopTracksByArtist(Action):
    def name(self) -> Text:
        return "action_top_tracks_by_artist"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artist_name = str(tracker.get_slot('artist'))

        if artist_name == "None" or artist_name == "":
            dispatcher.utter_message(text="You haven't provided an artist name.")
            return [SlotSet("artist", None)]

        token = get_token()

        artist = search_for_artist(token, artist_name)

        if artist == None:    
            output = f"I can't identify the top tracks by {artist_name}. Are you sure you spelled it correctly?"
            dispatcher.utter_message(text=output)
            return [SlotSet("artist", None)]
        else:
            artist_id = artist['id']
            songs = get_songs_by_artist(token, artist_id)

            if songs == None:
                output = f"I can't identify the top tracks by {artist['name']}."
                dispatcher.utter_message(text=output)
                return []
            else:
                output = f"These are the top tracks by {artist['name']}:\n\n"
                for song in songs:
                    duration =  milliseconds_to_string(song['duration'])
                    song_info = f"{song['title'].upper()}\n• duration: {duration}\n• popularity: {song['popularity']}\n\n"
                    output+=(song_info)
                dispatcher.utter_message(text=output)
                return []
            
class ActionTopAlbumsByArtist(Action):
    def name(self) -> Text:
        return "action_top_albums_by_artist"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artist_name = str(tracker.get_slot('artist'))

        if artist_name == "None" or artist_name == "":
            dispatcher.utter_message(text="You haven't provided an artist name.")
            return [SlotSet("artist", None)]

        token = get_token()

        artist = search_for_artist(token, artist_name)

        if artist == None:    
            output = f"I can't identify the top albums by {artist_name}. Are you sure you spelled it correctly?"
            dispatcher.utter_message(text=output)
            return [SlotSet("artist", None)]
        else:
            artist_id = artist['id']
            albums = get_albums_by_artist(token, artist_id)

            if albums == None:
                output = f"I can't identify the top albums by {artist['name']}."
                dispatcher.utter_message(text=output)
                return []
            else:
                output = f"These are the top albums by {artist['name']}:\n\n"
                for album in albums:
                    album_info = f"{album['title'].upper()}\n• release date: {album['release_date']}\n• total tracks: {album['total_tracks']}\n\n"
                    output+=(album_info)
                dispatcher.utter_message(text=output)
                return []
            
























class ActionSimilarArtists(Action):
    def name(self) -> Text:
        return "action_similar_artists"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artist_name = str(tracker.get_slot('artist'))

        if artist_name == "None" or artist_name == "":
            dispatcher.utter_message(text="You haven't provided an artist name.")
            return [SlotSet("artist", None)]

        token = get_token()

        artist = search_for_artist(token, artist_name)

        if artist == None:    
            output = f"I can't identify similar artists to {artist_name}. Are you sure you spelled it correctly?"
            dispatcher.utter_message(text=output)
            return [SlotSet("artist", None)]
        else:
            artist_id = artist['id']
            similar_artists = get_similar_artists(token, artist_id)

            if similar_artists == None:
                output = f"I can't identify any similar artist to {artist['name']}."
                dispatcher.utter_message(text=output)
                return []
            else:
                output = f"These are some similar artists to {artist['name']}:\n\n"
                for artist in similar_artists:
                    artist_info = f"{artist['name'].upper()}\n• followers: {artist['followers']}\n• genres: {artist['genres']}\n• popularity: {artist['popularity']}\n\n"
                    output+=(artist_info)
                dispatcher.utter_message(text=output)
                return []