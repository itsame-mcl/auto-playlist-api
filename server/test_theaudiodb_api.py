import pytest, random
from server.theaudiodb_api import *


# from https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://www.theaudiodb.com/api/v1/json/2/search.php' and 'params' not in kwargs:
        return MockResponse(None, 200)
    elif args[0] == 'https://www.theaudiodb.com/api/v1/json/2/search.php' and kwargs['params'] == {"s": "Queen"}:
        return MockResponse({"artists": [{"idArtist": "111238"}]}, 200)
    elif args[0] == 'https://theaudiodb.com/api/v1/json/2/album.php' and kwargs['params'] == {"i": 111238}:
        return MockResponse({"album": [
            {
                "idAlbum": "2109599",
                "idArtist": "111238"},
            {
                "idAlbum": "2109600",
                "idArtist": "111238"}]}, 200)
    elif args[0] == "https://theaudiodb.com/api/v1/json/2/track.php" and kwargs['params'] == {'m': 2109599}:
        return MockResponse({"track": [
            {
                "idTrack": "32724008",
                "idAlbum": "2109599"},
            {
                "idTrack": "32724009",
                "idAlbum": "2109599"}]}, 200)
    elif args[0] == "https://theaudiodb.com/api/v1/json/2/mvid.php" and kwargs['params'] == {"i": 111238}:
        return MockResponse({"mvids": [
            {
                "idArtist": "111238",
                "idAlbum": "2109600",
                "idTrack": "32724023",
                "strTrack": "The Miracle",
                "strTrackThumb": None,
                "strMusicVid": "https://www.youtube.com/watch?v=2DaY8-Mui0I",
                "strDescriptionEN": None
            }]}, 200)
    return MockResponse(None, 404)


@pytest.fixture(autouse=True)
def run_around_tests(mocker):
    mocker.patch('requests.get', mocked_requests_get)
    random.seed(1)
    yield


def test_check_tadb_health():
    check = check_tadb_health()
    assert check is True


def test_get_artist_id_from_name():
    id = get_artist_id_from_name("Queen")
    assert id == 111238


def test_get_random_album_id_from_artist_id():
    id = get_random_album_id_from_artist_id(111238)
    assert id == 2109599


def test_get_random_track_id_from_album_id():
    id = get_random_track_id_from_album_id(2109599)
    assert id == 32724008


def test_get_random_clip_from_artist_id():
    clip = get_random_clip_from_artist_id(111238)
    assert clip == {"title": "The Miracle", "suggested_youtube_url": "https://www.youtube.com/watch?v=2DaY8-Mui0I"}
