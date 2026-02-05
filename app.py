from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for sessions

# Dummy user database
users = {
    "bala": "password123",
    "admin": "adminpass"
}

# Simple HTML templates
login_page = """
<!doctype html>
<title>Login</title>
<h2>Login</h2>
<form method="post">
  Username: <input type="text" name="username"><br><br>
  Password: <input type="password" name="password"><br><br>
  <input type="submit" value="Login">
</form>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
"""

home_page = """
<!doctype html>
<title>Home</title>
<h2>Welcome {{ user }}!</h2>
<a href="{{ url_for('logout') }}">Logout</a>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template_string(login_page, error="Invalid credentials")
    return render_template_string(login_page)

@app.route("/home")
def home():
    if "user" in session:
        return render_template_string(home_page, user=session["user"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
