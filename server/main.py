import server.theaudiodb_api as tadb
import server.lyricsovh_api as lyrs
from fastapi import FastAPI
from fastapi_health import health


app = FastAPI()
app.add_api_route(
    "/", health(conditions=[tadb.check_tadb_health, lyrs.check_lyrs_health]))


def enhance_song_data(artist_name: str, song: dict) -> dict:
    lyrics = lyrs.get_lyrics_from_artist_and_title(artist_name, song['title'])
    return {"artist": artist_name, "title": song["title"], "suggested_youtube_url": song["suggested_youtube_url"], "lyrics": lyrics}


@app.get("/random/{artist_name}")
def get_random_song_from_artist(artist_name: str):
    artist_id = tadb.get_artist_id_from_name(artist_name)
    song = tadb.get_random_clip_from_artist_id(artist_id)
    enhanced_song = enhance_song_data(artist_name, song)
    return enhanced_song


@app.get("/songs/{artist_name}")
def get_all_songs_from_artist(artist_name: str):
    artist_id = tadb.get_artist_id_from_name(artist_name)
    songs = tadb.get_all_clips_from_artist_id(artist_id)
    ans = []
    for song in songs:
        try:
            enhanced_song = enhance_song_data(artist_name, song)
            ans.append(enhanced_song)
        except KeyError:
            pass
    return ans
