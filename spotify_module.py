from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json

#Funzione che restituisce il token di Spotify
def get_token():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

#Funzione che produce l'header di autenticazione
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    header = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=header)
    json_result = json.loads(result.content)["artists"]["items"]

    artist_info = {}

    if len(json_result) == 0:
        return artist_info
   
    artist = json_result[0]

    artist_info['name'] = artist['name']
    artist_info['genres'] = artist['genres']
    artist_info['followers'] = artist['followers']['total']
    artist_info['image'] = artist['images'][0]['url']

    return artist_info
    
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    header = get_auth_header(token)
    result = get(url, headers=header)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()

result = search_for_artist(token, "The Weeknd")
print(result)
#artist_id = result["id"]

#songs = get_songs_by_artist(token, artist_id)
#for idx, song in enumerate(songs):
 #   print(f"{idx + 1}. {song['name']}")




