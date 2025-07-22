import os
import requests
from app import app
from models import db, Streamer
from dotenv import load_dotenv
load_dotenv()

headers = {
    'Client-ID': os.getenv('TWITCH_CLIENT_ID'),
    'Authorization': os.getenv('TWITCH_AUTH')
}

streamers = [
    "KaiCenat", "evelone2004", "Ironmouse", "Ludwig", "Ninja", "Jynxzi",
    "vedal987", "Casimito", "CriticalRole", "Ibai", "Shlorox", "RanbooLive",
    "Jasontheween", "Gaules", "xQc", "Shroud", "summit1g", "caseoh_",
    "TheGrefg", "eliasn97", "HasanAbi", "Pestily", "plaqueboymax",
    "PirateSoftware", "NICKMERCS", "kkatamina", "PointCrow", "Fextralife",
    "AdinRoss", "Zizaran", "DDG", "Tumblurr", "Anomaly", "Trymacs", "Tfue",
    "tsukilin", "stableronaldo", "DarioMocciaTwitch", "Quin69", "iiTzTimmy",
    "JLTomy", "Aztecross", "Shylily", "Trainwreckstv", "AdmiralBahroo",
    "TimTheTatman", "Rubius", "PaymoneyWubby", "ZeratoR", "TheRealKnossi"
]

def seed_streamers():
    with app.app_context():
        for name in streamers:
            if Streamer.query.filter_by(name=name).first():
                print(f"Streamer '{name}' already exists. Skipping.")
                continue

            url = f'https://api.twitch.tv/helix/users?login={name}'
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if data['data']:
                    streamer_id = data['data'][0]['id']
                    img_url = data['data'][0]['profile_image_url']
                    new_streamer = Streamer(id=streamer_id,name=name, img=img_url, isFeatured=True)
                    db.session.add(new_streamer)
                    print(f"Added {name}")
                else:
                    print(f"No data found for {name}")
            else:
                print(f"Failed to fetch {name}: {response.status_code} - {response.text}")

        db.session.commit()
        print("Done seeding featured streamers.")

if __name__ == "__main__":
    seed_streamers()
