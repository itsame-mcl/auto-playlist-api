import server.theaudiodb_api as tadb
import server.lyricsovh_api as lyrs
from fastapi import FastAPI
from fastapi_health import health


app = FastAPI()
app.add_api_route(
    "/", health(conditions=[tadb.check_tadb_health, lyrs.check_lyrs_health]))


@app.get("/random/{artist_name}")
def get_random_song_from_artist(artist_name: str):
    artist_id = tadb.get_artist_id_from_name(artist_name)
    song = tadb.get_random_clip_from_artist_id(artist_id)
    lyrics = lyrs.get_lyrics_from_artist_and_title(artist_name, song['title'])
    return {"artist": artist_name, "title": song["title"], "suggested_youtube_url": song["suggested_youtube_url"], "lyrics": lyrics}
