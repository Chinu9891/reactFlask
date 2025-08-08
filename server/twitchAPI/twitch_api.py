# twitch_api.py
from dotenv import load_dotenv
import os, requests

class TwitchAPI:
    BASE_URL = "https://api.twitch.tv/helix"

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("TWITCH_CLIENT_ID")
        self.auth_token = os.getenv("TWITCH_AUTH")
        self.webhook_secret = os.getenv("TWITCH_WEBHOOK_SECRET")
        self.headers = {
            "Client-ID": self.client_id,
            "Authorization": self.auth_token
        }

    def subscribe_to_streamer(self, broadcaster_id):
        payload = {
            "type": "stream.online",
            "version": "1",
            "condition": {"broadcaster_user_id": broadcaster_id},
            "transport": {
                "method": "webhook",
                "callback": 'https://8d55936acc8e.ngrok-free.app/webhook',
                "secret": self.webhook_secret
            }
        }
        r = requests.post(f"{self.BASE_URL}/eventsub/subscriptions",
                          headers={**self.headers, "Content-Type": "application/json"},
                          json=payload)
        if r.status_code == 202:
            return {"success": True, "id": r.json()['data'][0]['id']}
        return {"success": False, "error": f"Failed: {r.text}"}

    def fetch_streamer(self, name):
        r = requests.get(f"{self.BASE_URL}/users?login={name}", headers=self.headers)
        if r.status_code == 200 and r.json()["data"]:
            data = r.json()["data"][0]
            return {"success": True, "streamer": {
                "id": data["id"], "name": data["display_name"], "img": data["profile_image_url"]
            }}
        return {"success": False, "error": "Streamer not found"}

    def list_subscriptions(self):
        r = requests.get(f"{self.BASE_URL}/eventsub/subscriptions", headers=self.headers)
        return [sub["id"] for sub in r.json()["data"]] if r.status_code == 200 else []

    def delete_subscription(self, subscription_id):
        r = requests.delete(f"{self.BASE_URL}/eventsub/subscriptions?id={subscription_id}", headers=self.headers)
        return r.status_code == 204
