from models.song import Song
from services.cache import Cache


def make_song(song_id: int = 1) -> Song:
    return Song(
        id=song_id,
        title="Yesterday",
        artist="The Beatles",
        url="https://genius.com/The-beatles-yesterday-lyrics",
    )


def test_search_cache():
    cache = Cache()

    songs = [make_song()]

    cache.search.set("yesterday", songs)

    result = cache.search.get("yesterday")

    assert result == songs


def test_song_cache():
    cache = Cache()

    song = make_song()

    cache.songs.set(song)

    result = cache.songs.get(song.id)

    assert result == song


def test_cache_clear():
    cache = Cache()

    cache.search.set("abc", [make_song()])
    cache.songs.set(make_song())

    cache.clear()

    assert cache.search.get("abc") is None
    assert cache.songs.get(1) is None