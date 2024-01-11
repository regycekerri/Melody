from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json
import random

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
        'id': artist_with_most_followers.get('id', 0),
        'followers': max_followers,
        'image': image_url
    }

    return artist_info

#Funzione che restituisce le canzoni più popolari di un dato artista
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    header = get_auth_header(token)
    result = get(url, headers=header)

    #Verifica il codice di stato nella risposta HTTP
    if result.status_code != 200:
        return None

    tracks = json.loads(result.content)["tracks"]

    songs_list = []

    for idx, song in enumerate(tracks):
        song_info = {
            'title': song['name'],
            'album': song['album']['name'],
            'album_release_date': song['album']['release_date'],
            'duration': song['duration_ms'],
            'popularity': song['popularity']
        }
        songs_list.append(song_info)
    
    return songs_list

#Funzione che restituisce gli album più recenti di un artista
def get_artist_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album%2Ccompilation&market=US&limit=10"
    header = get_auth_header(token)
    result = get(url, headers=header)

    #Verifica il codice di stato nella risposta HTTP
    if result.status_code != 200:
        return None

    albums = json.loads(result.content)["items"]

    albums_list = []

    for idx, album in enumerate(albums):
        album_info = {
            'title': album['name'],
            'release_date': album['release_date'],
            'total_tracks': album['total_tracks'],
            'uri': album['uri']
        }
        albums_list.append(album_info)

    return albums_list

#Funzione che restituisce alcuni artisti simili a quello specificato
def get_similar_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    header = get_auth_header(token)
    result = get(url, headers=header)

    # Verifica il codice di stato nella risposta HTTP
    if result.status_code != 200:
        return None

    artists = json.loads(result.content)["artists"]

    # Estrai casualmente 10 artisti da quelli disponibili
    random_artists = random.sample(artists, min(10, len(artists)))

    artists_list = []

    for idx, artist in enumerate(random_artists):
        artist_info = {
            'name': artist['name'],
            'followers': artist['followers']['total'],
            'genres': artist['genres'],
            'popularity': artist['popularity']
        }
        artists_list.append(artist_info)

    return artists_list


#print(get_similar_artists(get_token(), '1Xyo4u8uXC1ZmMpatF05PJ'))
