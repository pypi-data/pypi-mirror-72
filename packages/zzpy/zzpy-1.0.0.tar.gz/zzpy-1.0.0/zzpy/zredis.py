def decode_redis(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    if isinstance(value, (list, tuple, set)):
        return type(value)(map(decode_redis, value))
    return value


def redis_connect(redis_url=None):
    def get_url_from_params():
        try:
            from .zarg import get_param
            return get_param("REDIS_URL")
        except:
            return None

    if not redis_url:
        redis_url = get_url_from_params()
    assert redis_url, "缺失REDIS_URL"
    return RedisClient(redis_url)


class RedisClient:
    def __init__(self, url):
        import redis
        self.client = redis.from_url(url)

    def bpop_log(self, key, wait_log=None):
        if self.llen(key) <= 0:
            if wait_log:
                print(wait_log)
        return self.blpop(key)

    def get(self, key):
        return decode_redis(self.client.get(key))

    def set(self, key, value):
        return self.client.set(key, value)

    def expire(self, key, ttl):
        return self.client.expire(key, ttl)

    def set_expire(self, key, value, ttl):
        self.set(key, value)
        return self.expire(key, ttl)

    def rename(self, src, dst):
        self.client.rename(src, dst)

    def sall(self, key):
        return [decode_redis(it) for it in self.client.sunion(key)]

    def sadd(self, key, *value):
        return self.client.sadd(key, *value)

    def sismember(self, key, value):
        return self.client.sismember(key, value)

    def keys(self, pattern='*'):
        return list(map(decode_redis, self.client.keys(pattern)))

    def sdiff(self, keys, *args):
        return self.client.sdiff(keys, *args)

    def delete(self, *keys):
        return self.client.delete(*keys)

    def lpush(self, key, *values):
        return self.client.lpush(key, *values)

    def llen(self, key):
        return self.client.llen(key)

    def blpop(self, keys, timeout=0):
        return decode_redis(self.client.blpop(keys, timeout))[-1]
    
    def brpoplpush(self, src, dst, timeout=0):
        return decode_redis(self.client.brpoplpush(src, dst, timeout))

    def lpop(self, key):
        return decode_redis(self.client.lpop(key))

    def rpop(self, key):
        return decode_redis(self.client.rpop(key))

    def brpop(self, keys, timeout=0):
        return decode_redis(self.client.brpop(keys, timeout))[-1]

    def lall(self, key):
        return [decode_redis(it) for it in self.client.lrange(key, 0, -1)]

    def lrem(self, key, value):
        self.client.lrem(key, 0, value)

    def lpopall(self, key):
        items = [decode_redis(it) for it in self.client.lrange(key, 0, -1)]
        self.delete(key)
        return items

    def rpush(self, key, *values):
        return self.client.rpush(key, *values)
