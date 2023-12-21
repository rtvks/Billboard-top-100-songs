from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx" #Enter your own ID
CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxx" #Enter your own Secret 

YEAR = input("Which year do you want to travel to? Type the year in this format YYYY starting from 2006: ")

URL = f"https://www.billboard.com/charts/year-end/{YEAR}/hot-100-songs/"

response = requests.get(URL)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")

songs = soup.select(selector="li ul li h3")

songs_list = [song.getText() for song in songs]
print(songs_list)

res = [s.replace('\n\n\t\n\t\n\t\t\n\t\t\t\t\t', '') for s in songs_list]
result = [s.replace('\t\t\n\t\n', '') for s in res]

song_names = result
print(result)

sp = spotipy.Spotify(
auth_manager=SpotifyOAuth(
scope="playlist-modify-private",
redirect_uri="http://example.com/",
client_id=CLIENT_ID,
client_secret=CLIENT_SECRET,
show_dialog=True,
cache_path="tokenNew.txt"
)
)

user_id = sp.current_user()["id"]
print(user_id)

#Searching Spotify for songs by title
song_uris = []
year = YEAR

for song in song_names:
result = sp.search(q=f"track:{song} year:{year}", type="track")
print(result)
try:
uri = result["tracks"]["items"][0]["uri"]
song_uris.append(uri)
except IndexError:
print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{YEAR} Billboard Top 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
