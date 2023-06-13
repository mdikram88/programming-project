from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "a5be250a5bdb4922853ae7f6946c57d1"
CLIENT_SECRET = "874fb17462a8443a833908ba835018f6"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_headings = soup.select("div .o-chart-results-list-row-container ul li ul li h3")
song_names = [song.getText().strip() for song in song_names_headings]
# print(song_names)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
year = date.split("-")[0]
songs_uri = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{song} song not Found")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} BillBoard 100", public=False, description="Code Testing")


response = sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
print(response)
