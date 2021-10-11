from cloudevents.http import to_json
import redis
import time


class PubSub:

    def __init__(self, host='redis'):
        self._redis = redis.Redis(host=host)
        self._subscriptions = dict()

    def subscribe(self, user, channel):
        key = (user.id, channel)
        if key not in self._subscriptions:
            pubsub = self._redis.pubsub()
            pubsub.subscribe(channel)
            self._subscriptions[key] = pubsub
            print("subscriptions: {}".format(len(self._subscriptions)))

    def unsubscribe(self, user, channel):
        key = (user.id, channel)
        pubsub = self._subscriptions.get(key)
        if pubsub:
            pubsub.unsubscribe(channel)
            self._subscriptions.pop(key)

    def listen(self, user, channel):
        ps = self._subscriptions.get((user.id, channel))
        if ps is None:
            print("Not found: {}".format(user, channel))
            return None
        while True:
            msg = ps.get_message()
            if msg:
                msg_type = msg.get('type')
                msg_chan = msg.get('channel').decode()
                if msg_type == 'subscribe' and msg_chan == channel:
                    print("Skipping redis message")
                    continue
                print(f"Message: {msg}")
                return msg
            time.sleep(0.01)

    def publish(self, user, channel, message):
        self._redis.publish(channel, message)

    def publish2(self, user, channel, event):
        print("publish2()")
        print(to_json(event))
        self._redis.publish(channel, to_json(event))
