from dotenv import load_dotenv
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users
from . import db
import os
import requests

# ========= CONFIG =========
load_dotenv()

main = Blueprint('main', __name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ Missing GEMINI_API_KEY in environment variables")

GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

SYSTEM_PROMPT = """You are AI-CHATTER — a friendly, concise AI assistant for helping people and casual conversation.
Goals:
- Be clear, safe, and helpful.
- Answer directly first, then add brief extra tips if useful.
- If the user seems uncertain, ask one short follow-up question.
- Avoid overlong answers; prefer simple language.
- If you don’t know something, say so.
"""

# ========= ROUTES =========

@main.route('/')
def home():
    return render_template('index.html')


@main.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint using Gemini REST API"""
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "⚠️ No input provided"}), 400

    # Retrieve chat history
    history = session.get("chat_history", [])

    # Build conversation for Gemini
    contents = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}]
    for turn in history:
        contents.append({"role": "user", "parts": [{"text": turn["user"]}]})
        contents.append({"role": "model", "parts": [{"text": turn["bot"]}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    try:
        response = requests.post(
            GEMINI_URL,
            headers={"Content-Type": "application/json"},
            params={"key": GEMINI_API_KEY},
            json={"contents": contents}
        )
        response.raise_for_status()
        data = response.json()

        # Extract reply safely
        reply = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

        if not reply:
            reply = "⚠️ Sorry, I couldn’t generate a response. Please try again."

        # Update history
        history.append({"user": user_message, "bot": reply})
        session["chat_history"] = history[-20:]  # keep last 20 turns

        return jsonify({"reply": reply, "history_len": len(session["chat_history"])})

    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"❌ API error: {str(e)}"}), 500
    except Exception:
        return jsonify({"reply": "⚠️ Something went wrong, please try again..."}), 500


# ========= AUTH ROUTES =========

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = (request.form.get('username') or "").strip()
        email = (request.form.get('email') or "").strip()
        password = request.form.get('password') or ""

        if not username or not email or not password:
            flash('⚠️ All fields are required.', 'danger')
            return redirect(url_for('main.signup'))

        existing_user = Users.query.filter(
            (Users.username == username) | (Users.email == email)
        ).first()

        if existing_user:
            flash('⚠️ Username or email already exists!', 'danger')
            return redirect(url_for('main.signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        user = Users(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('✅ Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('signup.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or "").strip()
        password = request.form.get('password') or ""

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session.pop("chat_history", None)  # reset chat
            flash('✅ Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('❌ Invalid username or password!', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')


@main.route('/logout')
def logout():
    session.clear()
    flash('ℹ️ You have been logged out.', 'info')
    return redirect(url_for('main.home'))
