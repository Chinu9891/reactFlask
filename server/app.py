import hashlib
import hmac
import os

from flask import Flask, request, jsonify, session
from config import ApplicationConfig
from models import User, db, Streamer
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from flask_mail import Mail, Message

from twitchAPI.twitch_api import TwitchAPI

app = Flask(__name__)
twitch = TwitchAPI()
app.config.from_object(ApplicationConfig)
mail = Mail(app)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173", "http://localhost:5174"
])
server_session = Session(app)
db.init_app(app)
migrate = Migrate(app, db)


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
        return False

    expected_signature = 'sha256=' + hmac.new(secret.encode('utf-8'),message.encode('utf-8'),hashlib.sha256).hexdigest()

    provided_signature = headers.get('Twitch-Eventsub-Message-Signature', '')
    return hmac.compare_digest(expected_signature, provided_signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    if not verify_signature(request):
        return '', 403

    req = request.get_json(force=True)
    message_type = request.headers.get("Twitch-Eventsub-Message-Type")

    if message_type == "webhook_callback_verification":
        challenge = req.get("challenge")
        return challenge, 200

    elif message_type == "notification":
        streamer_id = req['event']['broadcaster_user_id']
        streamer = Streamer.query.get(streamer_id)

        for follower in streamer.followers.all():
            msg = Message(
                subject="Test Email",
                sender=app.config['MAIL_USERNAME'],
                recipients=[follower.email],
                body="This is a test email sent from Flask!"
            )
            mail.send(msg)

        return '', 204

    elif message_type == "revocation":
        return '', 204

    else:
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

    streamer_data = twitch.fetch_streamer(name)
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

    result = twitch.subscribe_to_streamer(streamer_id)

    if not result["success"]:
        return jsonify({"Error": result["error"]}), 400

    if not streamer:
        streamer = Streamer(id=streamer_id,name=strm.get('name'), img=strm.get('img'), isFeatured=False, subscription_id=result['id'])
        db.session.add(streamer)
    else:
        if streamer.subscription_id is None:
            streamer.subscription_id = result['id']

    if not user.followed_streamers.filter_by(id=streamer_id).first():
        user.followed_streamers.append(streamer)
        db.session.commit()

    return jsonify({}), 200

@app.route('/unfollow', methods=['POST'])
def unfollow():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()

    streamer = request.json.get('streamer')

    id = streamer.get('id')

    streamer = Streamer.query.get(id)


    user.followed_streamers.remove(streamer)

    if streamer.followers.first() is None:
        twitch.delete_subscription(streamer.subscription_id)
        streamer.subscription_id = None

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
    app.run(port=5000, debug=True, use_reloader=False)

