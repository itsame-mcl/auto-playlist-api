from os.path import normpath, basename, dirname
from random import randrange, sample, shuffle
import requests
import json


def parse_rudy_file(path: str) -> list:
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def generer_playlist_aleatoire(hostname: str, port: int, artistes: list, longueur: int) -> list:
    playlist = []
    i = 0
    while i < longueur and len(artistes) > 0:
        random_artiste_index = randrange(0, len(artistes))
        r = requests.get(
            "http://" + hostname + ":" + str(port) + "/random/" + artistes[random_artiste_index]['artiste'])
        if r.status_code == 200:
            playlist.append(r.json())
            i = i + 1  # On incrémente le compteur de chansons sélectionnées
        else:  # L'artiste n'a pas de chanson disponible
            artistes.remove(artistes[random_artiste_index])  # L'artiste ne sera pas réessayé
    return playlist


def generer_playlist_intelligente(hostname: str, port: int, artistes: list, longueur: int) -> list:
    playlist = []
    cache = {}
    for artiste in artistes:
        r = requests.get("http://" + hostname + ":" + str(port) + "/songs/" + artiste['artiste'])
        if r.status_code == 200:
            chansons = r.json()
            cache[artiste['artiste']] = {'poids': artiste['note'],
                                         'disponible': len(chansons), 'chansons': chansons}
    longueur_disponible = sum([artiste['disponible'] for artiste in cache.values()])
    if longueur_disponible <= longueur:  # S'il y a autant ou moins de chansons disponibles que de chansons demandées
        for artiste in cache.values():
            playlist.extend(artiste['chansons'])  # Toutes les chansons sont ajoutées à la playlist
    else:
        longueur_attribuee = 0
        phase_saturation = True
        while phase_saturation:
            longueur_a_attribuer = longueur - longueur_attribuee
            phase_saturation = False
            poids_total = sum([artiste['poids'] for artiste in cache.values()])
            for artiste in cache.values():
                if artiste['poids'] / poids_total >= artiste['disponible'] / longueur_a_attribuer:
                    phase_saturation = True
                    longueur_attribuee = longueur_attribuee + artiste['disponible']
                    playlist.extend(artiste['chansons'])  # Toutes ses chansons sont ajoutées à la playlist
                    artiste['poids'] = 0  # Le poids est mis à 0 pour que l'artiste ne compte plus
        longueur_a_attribuer = longueur - longueur_attribuee
        poids_total = sum([artiste['poids'] for artiste in cache.values()])
        for artiste in cache.values(): # Une fois les cas de saturation traités, on répartit selon les poids
            chansons_a_ajouter = min(round(artiste['poids'] * longueur_a_attribuer / poids_total),
                                     artiste['disponible'])
            playlist.extend(sample(artiste['chansons'], chansons_a_ajouter))
    shuffle(playlist)
    return playlist


def playlist_to_json(playlist: list, path: str) -> bool:
    playlist_json = {'playlist': playlist}
    try:
        with open(path, 'w') as file:
            json.dump(playlist_json, file)
    except IOError:
        return False
    return True


def random_playlist_from_json(hostname: str, port: int, json_path: str, longueur: int, smart: bool) -> bool:
    try:
        input = parse_rudy_file(json_path)
        output_path = dirname(normpath(json_path)) + "/playlist_" + basename(normpath(json_path))
        if smart:
            playlist = generer_playlist_intelligente(hostname, port, input, longueur)
        else:
            playlist = generer_playlist_aleatoire(hostname, port, input, longueur)
        res = playlist_to_json(playlist, output_path)
    except IOError:
        return False
    return res
