import os
import requests
from dotenv import load_dotenv
load_dotenv()

headers = {
    'Client-ID': os.getenv('TWITCH_CLIENT_ID'),
    'Authorization': os.getenv('TWITCH_AUTH')  # Must be "Bearer <token>"
}

def subscribe_to_streamer(broadcaster_id):
    eventSubHeaders = {
        "Client-ID": os.getenv('TWITCH_CLIENT_ID'),
        "Authorization": os.getenv('TWITCH_AUTH'),
        "Content-Type": "application/json"
    }

    eventSubPayload = {
        "type": "stream.online",
        "version": "1",
        "condition": {
            "broadcaster_user_id": broadcaster_id,
        },
        "transport": {
            "method": "webhook",
            "callback": "https://ef0144da54fd.ngrok-free.app/webhook",
            "secret": os.getenv('TWITCH_WEBHOOK_SECRET')
        }
    }

    response = requests.post("https://api.twitch.tv/helix/eventsub/subscriptions", headers=eventSubHeaders, json=eventSubPayload)
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:", response.json())
    except Exception:
        print("Raw Response:", response.text)


def fetch_streamer(name):

    url = f'https://api.twitch.tv/helix/users?login={name}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            req_data = {
                "id" : data['data'][0]['id'],
                "name" : data['data'][0]['display_name'],
                "img" : data['data'][0]['profile_image_url'],
            }
            return {"success": True, "streamer": req_data}
        else:
            return {"success": False, "error": f"No streamer found with name '{name}'"}
    else:
        return {
            "success": False,
            "error": f"Failed to fetch {name}: {response.status_code}",
            "details": response.text
        }


def list_eventsub_subscriptions():
    url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        return [sub['id'] for sub in data['data']]
    else:
        print(f"Failed to fetch subscriptions: {response.status_code} {response.text}")

def delete_eventsub_subscription(subscription_id):
    url = f"https://api.twitch.tv/helix/eventsub/subscriptions?id={subscription_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Successfully deleted subscription ID: {subscription_id}")
    else:
        print(f"Failed to delete subscription: {response.status_code} {response.text}")



if __name__ == '__main__':
    for id in list_eventsub_subscriptions():
        delete_eventsub_subscription(id)
    #subscribe_to_streamer("428105098")
