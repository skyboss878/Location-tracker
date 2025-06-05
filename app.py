from flask import Flask, request, render_template, send_file, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super-secret-key-change-this'  # change this to something private

USERNAME = 'skyboss878'
PASSWORD = 'mypassword123'  # 🔒 change this!

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/log", methods=["POST"])
def log_location():
    data = request.get_json()
    if data:
        log_entry = f"{datetime.utcnow()} | Lat: {data.get('latitude')} | Lon: {data.get('longitude')} | Time: {data.get('timestamp')}\n"
        with open("shared_text.txt", "a") as f:
            f.write(log_entry)
    return "", 204

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("view_locations"))
        else:
            return "❌ Access denied. Wrong username or password.", 403
    return '''
    <form method="post">
        <h2>🔐 Login</h2>
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    '''

@app.route("/view")
def view_locations():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    try:
        return send_file("shared_text.txt", mimetype="text/plain")
    except FileNotFoundError:
        return "No locations logged yet."

@app.route("/logout")
def logout():
    session.clear()
    return "Logged out."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
          
