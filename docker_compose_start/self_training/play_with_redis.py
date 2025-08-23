from redis import Redis
import names
from random import randint

cache = Redis(host="redis", port=6379, decode_responses=True)

name = names.get_full_name()
age = randint(18, 95)

cache.set(name, age)

for key in cache.scan_iter():
    print(key, cache.get(key))
