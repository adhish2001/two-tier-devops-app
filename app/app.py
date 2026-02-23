from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # needed for sessions


def get_random_anime():
    url = "https://api.jikan.moe/v4/random/anime"
    data = requests.get(url).json()["data"]

    return {
        "title": data["title"],
        "image": data["images"]["jpg"]["image_url"],
        "season": data["season"],
        "year": data["year"]
    }


@app.route("/", methods=["GET", "POST"])
def game():

    # 🎮 Start new game if no session data
    if "anime" not in session:
        session["anime"] = get_random_anime()
        session["attempts"] = 0

    anime = session["anime"]
    result = None

    if request.method == "POST":
        guess_year = request.form["year"]
        guess_season = request.form["season"]

        session["attempts"] += 1

        if guess_year == str(anime["year"]) and guess_season == anime["season"]:
            result = f"✅ Correct in {session['attempts']} guesses!"
        else:
            result = "❌ Try again"

    return render_template_string(f"""
    <html>
    <body style="font-family:Arial; text-align:center; padding:40px;">
        <h1>Guess the Anime Release 📺</h1>

        <img src="{anime['image']}" width="300"><br><br>
        <h2>{anime['title']}</h2>

        {"<h2>"+result+"</h2>" if result else ""}

        <form method="POST">
            <label>Year:</label><br>
            <input type="number" name="year" required><br><br>

            <label>Season:</label><br>
            <select name="season">
                <option>winter</option>
                <option>spring</option>
                <option>summer</option>
                <option>fall</option>
            </select><br><br>

            <button type="submit">Submit Guess</button>
        </form>

        <br>
        <a href="/new">New Game</a>
    </body>
    </html>
    """)


@app.route("/new")
def new_game():
    session.pop("anime", None)
    session.pop("attempts", None)
    return redirect(url_for("game"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)