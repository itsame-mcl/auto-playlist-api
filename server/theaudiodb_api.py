import requests


def get_artist_id_from_name(artist_name: str) -> int:
    payload = {"s": artist_name}
    r = requests.get(
        "https://www.theaudiodb.com/api/v1/json/2/search.php", params=payload)
    if r.status_code == 200:
        r = r.json()
        if r['artists'] is not None:
            return r.json()['artists'][0]['idArtist']
        else:
            raise KeyError
    else:
        raise ConnectionError
