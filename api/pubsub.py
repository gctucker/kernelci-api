import redis
import time


class PubSub:

    def __init__(self, host='redis'):
        self._redis = redis.Redis(host=host)
        self._ps = self._redis.pubsub()

    def subscribe(self, channel):
        self._ps.subscribe(channel)

    def listen(self):
        #for item in self._ps.listen():
        #    return item
        while True:
            msg = self._ps.get_message()
            if msg:
                return msg
            time.sleep(0.01)

    def publish(self, channel, message):
        self._redis.publish(channel, message)
