from redis import Redis

cache = Redis(host="redis", port=6379)
cache.set("exemple", 5)
print(int(cache.get("exemple")) ** 2)

