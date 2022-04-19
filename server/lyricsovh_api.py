import requests


def check_lyrs_health() -> bool:
    r = requests.get("https://api.lyrics.ovh/v1/Toto/Africa")
    if r.status_code == 200:
        return True
    else:
        return False


def get_lyrics_from_artist_and_title(artist: str, title: str) -> str:
    endpoint = "https://api.lyrics.ovh/v1/" + artist + "/" + title
    r = requests.get(endpoint)
    if r.status_code == 200:
        r = r.json()
        return r['lyrics']
    elif r.status_code == 404:
        raise KeyError
    else:
        raise ConnectionError
