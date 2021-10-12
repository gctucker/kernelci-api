from cloudevents.http import CloudEvent, from_http, from_json
import requests
import sys

user_tokens = {
    'user': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIn0.ABlSQXWsEqa9X6FdrQJy-rYYM2IlJ6YNSgQj39A972U',
    'bob': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2IifQ.KHkILtsJaCmueOfFCj79HGr6kHamuZFdB1Yz_5GqcC4'
}


user = sys.argv[1] if len(sys.argv) > 1 else 'bob'
token = user_tokens[user]
headers = {'Authorization': f"Bearer {token}"}

requests.get("http://localhost:8000/subscribe/hey", headers=headers)

try:
    while True:
        raw_event = requests.get(
            "http://localhost:8000/listen/hey",
            headers=headers
        )
        json_data = raw_event.json().get('data')
        event = from_json(json_data)
        print(f"Data: {event.data}")
        print(f"Message: {event.data.get('message')}")
except Exception as e:
    print(e)
finally:
    pass

requests.get("http://localhost:8000/unsubscribe/hey", headers=headers)

print("Done.")
