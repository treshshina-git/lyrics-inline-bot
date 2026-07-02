from bot.services.cache import TTLCache


def test_cache_set_get():
    cache = TTLCache[int](ttl=1)

    cache.set("a", 123)
    assert cache.get("a") == 123


def test_cache_expiry():
    cache = TTLCache[int](ttl=0)

    cache.set("a", 123)
    assert cache.get("a") is None