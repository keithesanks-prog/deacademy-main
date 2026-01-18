import requests
access_token = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzY4NjEyMDAyLCJqdGkiOiIyODBlZTUzNy0xN2MzLTRhMzktOTFhNy0yYjA2YzM4OTA4OTEiLCJ1c2VyX3V1aWQiOiIxYjMzNzQxMi1lNjZiLTQ2YmEtYjJkZi05MTMyZmNiNDlmOWMifQ.75jfjFZmzfZ56AcUPHmyTe61g_1jONIp_jhFDp6EMjiENsFPD_E7UobFI9ctM6kDpQvy3sntweQH8mZgFM7AGA"
uri = "https://api.calendly.com/users/me"
header = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
response = requests.get(url=uri,headers=header)

# print(response.json().get("resource").get("current_organization"))

def get_org_id():
    uri = "https://api.calendly.com/users/me"
    header = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url=uri,headers=header)
    return response.json().get("resource").get("current_organization")

org_id = get_org_id()
url = "https://api.calendly.com/event_types?organization="f"{org_id}"
response = requests.get(url=url,headers=header)
# Get the list of Event Types first (Parse JSON!)
response_types = requests.get(url=url, headers=header)
event_types_list = response_types.json().get("collection", [])

print(f"Found {len(event_types_list)} Event Types. Fetching events for each...")

for event_type in event_types_list:
    # Extract the URI of the specific event type
    type_uri = event_type.get("uri")
    
    # Correct URL syntax: Use '?' for parameters usually, but wait... 
    # Valid filter: scheduled_events?organization=...&status=active
    # There isn't a direct 'event_type' filter on the list endpoint usually, 
    # but assuming the user wants to filter, we'll try to just list ALL events 
    # for the organization as that is the standard pattern.
    
    # However, to preserve the user's intent of looping:
    print(f"Checking events for type: {event_type.get('name')}")
    
    # NOTE: The simplest way to get events is just asking for all of them:
    events_url = "https://api.calendly.com/scheduled_events"
    params = {
        "organization": org_id,
        # "status": "active" 
    }
    
    events_resp = requests.get(events_url, headers=header, params=params)
    events_list = events_resp.json().get("collection", [])
    
    if not events_list:
        print("  No events found.")
    else:
        for event in events_list:
            print(f"  Found Event: {event.get('name')}")
    
    # Break after one success since we are listing ALL events for the Org regardless of type
    # (The API doesn't filter by EventType URI in the simple list call)
    break

# print(response.json().get("collection"))

