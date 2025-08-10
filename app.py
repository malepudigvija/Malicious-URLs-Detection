import sqlite3
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from flask_cors import CORS
from flask import session, redirect, url_for
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from werkzeug.security import generate_password_hash
from url_checker import check_url_heuristics


from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns




app = Flask(__name__)
app.secret_key = 'supersecretkey123456' 
users = 'malicious-url-detector/users.db' 
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

CORS(app)




# Load the trained model and vectorizer
model = joblib.load("models/malicious_url_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
# ============================
# User Signup Route
# ============================
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409
    finally:
        conn.close()
# ============================
# User Login Route
# ============================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/')
def home():
    return render_template("dashboard2.html")


'''@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url = data["url"]

    # Transform URL using the trained vectorizer
    url_vectorized = vectorizer.transform([url])

    # Predict
    prediction = model.predict(url_vectorized)[0]
    """result = "Malicious" if prediction == 1 else "Safe"""
    if prediction == 0:
        result = "✅ Benign (Safe)"
    elif prediction == 1:
        result = "⚠️ Phishing"
    elif prediction == 2:
        result = "🚨 Defacement"
    else:
        result = "❓ Unknown"

    

    return jsonify({"url": url, "result": result})'''
@app.route('/predict', methods=['POST'])
def predict():
        data = request.json
        url = data.get("url", "")

        # 1. Run heuristic checks first
        suspicious, reasons = check_url_heuristics(url)
        if suspicious:
            return jsonify({
                "url": url,
                "result": "⚠️ Suspicious (Heuristic)",
                "reasons": reasons,
                "method": "heuristic"
            })

        # 2. If heuristics look fine, run ML model
        url_vectorized = vectorizer.transform([url])
        prediction = model.predict(url_vectorized)[0]

        if prediction == 0:
            result = "✅ Benign (Safe)"
        elif prediction == 1:
            result = "⚠️ Phishing"
        elif prediction == 2:
            result = "🚨 Defacement"
        else:
            result = "❓ Unknown"

        return jsonify({
            "url": url,
            "result": result,
            "reasons": ["ML model decision"],
            "method": "ml"
        })
        return render_template('result.html')
# ============================
# User Logout Route
# ============================
@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('dashboard2.html') 

# ============================
# Model_performance
# ============================
@app.route('/model_performance')
def model_performance():
    # Example (you replace y_test and y_pred with your actual data)
    y_test = [0, 1, 0, 1, 0, 1, 0, 1]    # 0 = benign, 1 = malicious
    y_pred = [0, 1, 0, 0, 0, 1, 0, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    return render_template('model_performance.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1)

# ============================
#profile
# ============================
@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    user_id = data.get('user_id')  # Assume you're sending user_id from frontend
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([user_id, name, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        update_query = """
        UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?
        """
        cursor.execute(update_query, (name, email, hashed_password, user_id))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
