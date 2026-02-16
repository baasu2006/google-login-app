from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from google_auth_oauthlib.flow import Flow
import os, requests

app = Flask(__name__)
app.secret_key = "supersecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db = SQLAlchemy(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]

# ---------------- DATABASE ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    preference = db.Column(db.String(200))

with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("login.html")

# ----------- NORMAL REGISTER ------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed = generate_password_hash(request.form["password"])
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=hashed
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html")

# ----------- NORMAL LOGIN ------------
@app.route("/login", methods=["POST"])
def login():
    user = User.query.filter_by(email=request.form["email"]).first()
    if user and check_password_hash(user.password, request.form["password"]):
        session["user_id"] = user.id
        return redirect(url_for("preferences"))
    return "Invalid credentials"

# ----------- GOOGLE LOGIN ------------
@app.route("/google_login")
def google_login():
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:5000/google_callback"
    )
    auth_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(auth_url)

@app.route("/google_callback")
def google_callback():
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        state=session["state"],
        redirect_uri="http://127.0.0.1:5000/google_callback"
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"access_token": credentials.token}
    ).json()

    user = User.query.filter_by(email=userinfo["email"]).first()

    if not user:
        user = User(
            username=userinfo["name"],
            email=userinfo["email"],
            password=""
        )
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    return redirect(url_for("preferences"))

# ----------- PREFERENCES ------------
@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    if request.method == "POST":
        user = User.query.get(session["user_id"])
        user.preference = request.form["preference"]
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("preferences.html")

# ----------- DASHBOARD ------------
@app.route("/dashboard")
def dashboard():
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
