import requests
from random import randrange


def check_api_health() -> bool:
    r = requests.get("https://www.theaudiodb.com/api/v1/json/2/search.php")
    if r.status_code == 200:
        return True
    else:
        return False


def get_artist_id_from_name(artist_name: str) -> int:
    payload = {"s": artist_name}
    r = requests.get(
        "https://www.theaudiodb.com/api/v1/json/2/search.php", params=payload)
    if r.status_code == 200:
        r = r.json()
        if r['artists'] is not None:
            return r['artists'][0]['idArtist']
        else:
            raise KeyError
    else:
        raise ConnectionError


def get_random_album_id_from_artist_id(artist_id: int) -> int:
    payload = {"i": artist_id}
    r = requests.get(
        "https://theaudiodb.com/api/v1/json/2/album.php", params=payload)
    if r.status_code == 200:
        r = r.json()
        if r['album'] is not None:
            random_album_index = randrange(0, len(r['album']))
            return r['album'][random_album_index]['idAlbum']
    else:
        raise ConnectionError


def get_random_track_name_from_album_id(album_id: int) -> str:
    payload = {"m": album_id}
    r = requests.get(
        "https://theaudiodb.com/api/v1/json/2/track.php", params=payload)
    if r.status_code == 200:
        r = r.json()
        if r['track'] is not None:
            random_track_index = randrange(0, len(r['track']))
            return r['track'][random_track_index]['strTrack']
    else:
        raise ConnectionError
