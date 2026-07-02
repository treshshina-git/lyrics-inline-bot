from models.song import Song
from services.formatter import formatter


def make_song() -> Song:
    return Song(
        id=1,
        title="Yesterday",
        artist="The Beatles",
        url="https://genius.com/The-beatles-yesterday-lyrics",
        artwork_url="https://example.com/art.jpg",
        album="Help!",
        release_date="1965",
    )


def test_inline_title():
    song = make_song()

    assert formatter.inline_title(song) == "Yesterday — The Beatles"


def test_inline_description():
    song = make_song()

    assert formatter.inline_description(song) == "Help! • 1965"


def test_message():
    song = make_song()

    message = formatter.message(song)

    assert "Yesterday" in message
    assert "The Beatles" in message
    assert "Help!" in message
    assert "1965" in message
    assert "genius.com" in message


def test_empty():
    text = formatter.empty("test")

    assert "test" in text


def test_error():
    assert formatter.error()