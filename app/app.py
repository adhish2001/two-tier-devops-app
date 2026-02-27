from flask import Flask, request, render_template_string, session
import requests

app = Flask(__name__)
app.secret_key = "dev"

MAX_GUESSES = 3


def get_random_anime():
    data = requests.get("https://api.jikan.moe/v4/random/anime").json()["data"]
    return data["title"], data["images"]["jpg"]["image_url"], data["season"], data["year"]


@app.route("/", methods=["GET", "POST"])
def game():

    # Initialize game once
    if "title" not in session:
        title, image, season, year = get_random_anime()
        session["title"] = title
        session["image"] = image
        session["season"] = season
        session["year"] = year
        session["guesses"] = 0

    result = ""
    reveal = False

    if request.method == "POST":
        guess_year = request.form["year"]
        guess_season = request.form["season"]

        session["guesses"] += 1

        if (
            guess_year == str(session["year"])
            and guess_season == session["season"]
        ):
            result = "✅ Correct!"
            reveal = True

        elif session["guesses"] >= MAX_GUESSES:
            result = "❌ Out of guesses!"
            reveal = True
        else:
            result = f"❌ Wrong — {MAX_GUESSES - session['guesses']} tries left"

    if reveal:
        answer = f"{session['season'].title()} {session['year']}"
        session.clear()
    else:
        answer = ""

    return render_template_string(f"""
    <html>
    <body style="font-family:Arial; text-align:center; padding:40px;">
        <h1>Guess the Anime Release 📺</h1>

        <img src="{session.get('image', '')}" width="300"><br><br>
        <h2>{session.get('title', '')}</h2>

        <h3>{result}</h3>
        <h3>{answer}</h3>

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

        <br><a href="/">New Game</a>
    </body>
    </html>
    """)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)