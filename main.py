import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

user_input = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")
billboard_url = f"https://www.billboard.com/charts/hot-100/{user_input}"
spotify_client_id = "43ddf3e907834af3ba49176450721c5f"
spotify_client_secret = "1ed2f43e830d49188c41c12043f8b7a6"
spotify_redirect_uri = "http://example.com"

response = requests.get(billboard_url)
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")
song_tags = soup.find_all(name="h3", class_="a-no-trucate")
song_titles = [x.getText().strip() for x in song_tags]
# print(len(song_titles))
# print(song_titles)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri=spotify_redirect_uri,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))

user_id = sp.current_user()["id"]

song_uris = []
for x in song_titles:
    song = sp.search(q=f"track: {x} year: {user_input[:4]}", type='track')
    try:
        uri = song["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{x} doesn't exist in Spotify. Skipped")

print(len(song_uris))
print(song_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} Billboard 100", public=False)
playlist_id = playlist["uri"]
print(playlist_id)

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)



