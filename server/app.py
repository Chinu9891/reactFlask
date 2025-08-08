import hashlib
import hmac
import os
import threading

from flask import Flask, request, jsonify, session
from config import ApplicationConfig
from models import User, db, Streamer
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from flask_mail import Mail, Message
from twitchAPI.twitchAPI import fetch_streamer, subscribe_to_streamer, delete_eventsub_subscription, list_eventsub_subscriptions
import asyncio
import websockets

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
mail = Mail(app)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173", "http://localhost:5174"
])
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

def verify_signature(req):
    secret = os.getenv('TWITCH_WEBHOOK_SECRET')
    headers = req.headers
    raw_body = req.get_data()

    try:
        message = (
            headers['Twitch-Eventsub-Message-Id'] +
            headers['Twitch-Eventsub-Message-Timestamp'] +
            raw_body.decode('utf-8'))
    except KeyError as e:
        print(f"Missing header {e}")
        return False

    expected_signature = 'sha256=' + hmac.new(secret.encode('utf-8'),message.encode('utf-8'),hashlib.sha256).hexdigest()

    provided_signature = headers.get('Twitch-Eventsub-Message-Signature', '')
    return hmac.compare_digest(expected_signature, provided_signature)

# loop = asyncio.new_event_loop()
# connected_clients = set()
# async def send_msg(message):
#     if connected_clients:
#         await asyncio.gather(*[client.send(message) for client in connected_clients])
#     else:
#         print("No connected clients to send message to.")
#
# async def ws_handler(websocket):
#     print("Client connected")
#     connected_clients.add(websocket)
#     try:
#         async for message in websocket:
#             print(f"Received from client: {message}")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         connected_clients.remove(websocket)
#         print("Client disconnected")
#
# async def start_ws():
#     server = await websockets.serve(ws_handler, "localhost", 8765)
#     print("WebSocket server running on ws://localhost:8765")
#     await asyncio.Future()  # Run forever
#
# def run_websocket_server():
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(start_ws())



@app.route('/webhook', methods=['POST'])
def webhook():
    if not verify_signature(request):
        print("Signature mismatch!")
        return '', 403

    req = request.get_json(force=True)
    message_type = request.headers.get("Twitch-Eventsub-Message-Type")

    if message_type == "webhook_callback_verification":
        challenge = req.get("challenge")
        print(f"Verification challenge received: {challenge}")
        return challenge, 200

    elif message_type == "notification":
        print("Notification received:")
        #asyncio.run_coroutine_threadsafe(send_msg("BATCHEST!"), loop)
        print(req)
        return '', 204

    elif message_type == "revocation":
        print("Subscription revoked:")
        print(req)
        return '', 204

    else:
        print("Unhandled message type or invalid request.")
        return '', 400

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    user_exist = User.query.filter_by(email=email).first() is not None

    if user_exist:
        return jsonify({"Error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": email
    })

@app.route('/favorites', methods=['GET'])
def favorites():
    user_id = session.get('user_id')

    user = User.query.filter_by(id=user_id).first()

    followed = user.followed_streamers.all()

    followed_data = [
        {
            "id": streamer.id,
            "name": streamer.name,
            "img": streamer.img,
        }
        for streamer in followed
    ]

    return jsonify({"favorites": followed_data})


@app.route('/getStreamer', methods=['GET'])
def get_streamer():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"Error": "Unauthorized"}), 401

    name = request.args.get('name')
    if not name:
        return jsonify({"Error": "Missing streamer name"}), 400

    streamer_data = fetch_streamer(name)
    if streamer_data['success']:
        return jsonify(streamer_data), 200
    else:
        return jsonify({"Error": streamer_data['error']}), 400

@app.route('/follow', methods=['POST'])
def follow():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()

    strm = request.json.get('streamer')

    streamer_id = strm.get('id')

    streamer = Streamer.query.get(streamer_id)

    if not streamer:
        streamer = Streamer(id=streamer_id,name=strm.get('name'), img=strm.get('img'), isFeatured=False)
        db.session.add(streamer)

    if not user.followed_streamers.filter_by(id=streamer_id).first():
        user.followed_streamers.append(streamer)
        db.session.commit()

    subscribe_to_streamer(streamer_id)

    return jsonify({}), 200

@app.route('/unfollow', methods=['POST'])
def unfollow():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()

    streamer = request.json.get('streamer')

    id = streamer.get('id')

    streamer = Streamer.query.get(id)


    user.followed_streamers.remove(streamer)
    db.session.commit()

    return jsonify({}), 200

@app.route('/@me')
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"Error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email,
    })

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user_id", None)
    return {}, 200

@app.route('/email', methods=['POST'])
def email():
    users = User.query.with_entities(User.email).all()
    emails = [email for (email,) in users]

    for recipient in emails:
        msg = Message(
            subject="Test Email",
            sender=app.config['MAIL_USERNAME'],
            recipients=[recipient],
            body="This is a test email sent from Flask!"
        )
        mail.send(msg)

    return {}, 200

@app.route('/featured', methods=['GET'])
def featured():
    featured_streamers = Streamer.query.filter_by(isFeatured=True).all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "img": s.img
        }
        for s in featured_streamers
    ]), 200

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"Error": "Invalid email or password"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"Error": "Invalid email or password"}), 401

    session.permanent = True
    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email,
    })

if __name__ == '__main__':
    #ws_thread = threading.Thread(target=run_websocket_server)
    #ws_thread.daemon = True
    #ws_thread.start()

    # Main Flask app
    app.run(port=5000, debug=True, use_reloader=False)

