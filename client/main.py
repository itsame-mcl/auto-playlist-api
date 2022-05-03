from os.path import normpath, basename, dirname
from random import randrange
import requests
import json


def parse_rudy_file(path: str) -> list:
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def generer_playlist_aleatoire(artistes: list, longueur: int) -> list:
    playlist = []
    for i in range(0, longueur):
        random_artiste_index = randrange(0, len(artistes))
        r = requests.get("http://localhost:8000/random/" + artistes[random_artiste_index]['artiste'])
        if r.status_code == 200:
            playlist.append(r.json())
        else:
            i = i - 1
            artistes.remove(artistes[random_artiste_index])
    return playlist


def playlist_to_json(playlist: list, path: str) -> bool:
    playlist_json = {'playlist': playlist}
    try:
        with open(path, 'w') as file:
            json.dump(playlist_json, file)
    except IOError:
        return False
    return True


def random_playlist_from_json(json_path: str, longueur: int = 20) -> bool:
    try:
        input = parse_rudy_file(json_path)
        output_path = dirname(normpath(json_path)) + "/playlist_" + basename(normpath(json_path))
        playlist = generer_playlist_aleatoire(input, longueur)
        res = playlist_to_json(playlist, output_path)
    except IOError:
        return False
    return res
