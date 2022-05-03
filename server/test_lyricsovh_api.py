import pytest
from server.lyricsovh_api import check_lyrs_health, get_lyrics_from_artist_and_title


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.lyrics.ovh/v1/Toto/Africa':
        return MockResponse({"lyrics":"I hear the drums echoing tonight"}, 200)
    elif args[0] == 'https://api.lyrics.ovh/v1/France Gall/Blablacar':
        return MockResponse({"error":"No lyrics found"}, 404)
    return MockResponse(None, 404)


@pytest.fixture(autouse=True)
def run_around_tests(mocker):
    mocker.patch('requests.get', mocked_requests_get)
    yield


def test_check_lyrs_health():
    check = check_lyrs_health()
    assert check is True


def test_get_lyrics_from_artist_and_title_exists():
    lyrics = get_lyrics_from_artist_and_title("Toto","Africa")
    assert lyrics == "I hear the drums echoing tonight"


def test_get_lyrics_from_artist_and_title_does_not_exists():
    with pytest.raises(KeyError):
        lyrics = get_lyrics_from_artist_and_title("France Gall","Blablacar")
