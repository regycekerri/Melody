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

#Funzione che ricerca le informazioni di un artista
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    header = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=5"

    query_url = url + query
    result = get(query_url, headers=header)
    #Verifica il codice di stato nella risposta HTTP
    if result.status_code != 200:
        return None
    
    artists = result.json().get("artists", {}).get("items", [])
    #Verifica che gli artisti non siano assenti
    if not artists:
        return None

    #Ricerca l'artista con più follower
    max_followers = artists[0].get('followers', {}).get('total', 0)
    artist_with_most_followers = artists[0]

    for artist in artists[1:]:
        followers = artist.get('followers', {}).get('total', 0)
        if followers > max_followers:
            max_followers = followers
            artist_with_most_followers = artist

    #Verifica la presenza di immagini
    images = artist_with_most_followers.get('images', [])
    image_url = images[0]['url'] if images else None

    artist_info = {
        'name': artist_with_most_followers.get('name', ''),
        'genres': artist_with_most_followers.get('genres', []),
        'followers': max_followers,
        'image': image_url
    }

    return artist_info