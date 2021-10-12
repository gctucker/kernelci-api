from cloudevents.http import CloudEvent, to_binary, to_structured, from_json
import requests

attributes = {
    "type": "api.kernelci.org",
    "source": "https://api.kernelci.org/",
}
data = {"message": "KernelCI API CloudEvent"}
event = CloudEvent(attributes, data)
headers, body = to_structured(event)

print("Headers:")
print(headers)

print("Body:")
print(body)

event2 = from_json(body)
print("Event again:")
print(event2)
print(f"Message: {event2.data['message']}")

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib2IifQ.KHkILtsJaCmueOfFCj79HGr6kHamuZFdB1Yz_5GqcC4'
headers['Authorization'] = f"Bearer {token}"
requests.post("http://localhost:8000/publish2/hey", data=body, headers=headers)

print("Done.")
