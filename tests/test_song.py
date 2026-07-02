from models.song import Song


def test_caption():
    song = Song(
        id=1,
        title="Yesterday",
        artist="The Beatles",
        url="https://example.com",
    )

    assert song.caption == "Yesterday — The Beatles"


def test_cache_key():
    song = Song(
        id=123,
        title="Song",
        artist="Artist",
        url="https://example.com",
    )

    assert song.cache_key == "123"


def test_callback_data():
    song = Song(
        id=999,
        title="Song",
        artist="Artist",
        url="https://example.com",
    )

    assert song.to_callback_data() == "song:999"


def test_from_callback_data():
    songs = [
        Song(
            id=1,
            title="One",
            artist="Artist",
            url="https://example.com/1",
        ),
        Song(
            id=2,
            title="Two",
            artist="Artist",
            url="https://example.com/2",
        ),
    ]

    song = Song.from_callback_data("song:2", songs)

    assert song is not None
    assert song.id == 2


def test_invalid_callback_data():
    songs = []

    assert Song.from_callback_data("invalid", songs) is None
    assert Song.from_callback_data("song:test", songs) is None
    assert Song.from_callback_data("song:", songs) is None