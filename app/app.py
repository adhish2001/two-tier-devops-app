from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

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
    if request.method == "POST":
        correct_year = request.form["correct_year"]
        correct_season = request.form["correct_season"]
        guess_year = request.form["year"]
        guess_season = request.form["season"]

        result = "✅ Correct!" if (guess_year == correct_year and guess_season == correct_season) else "❌ Wrong"

        return f"""
        <h1>{result}</h1>
        <p>Correct answer: {correct_season.title()} {correct_year}</p>
        <a href="/">Play again</a>
        """

    anime = get_random_anime()

    return render_template_string(f"""
    <html>
    <body style="font-family:Arial; text-align:center; padding:40px;">
        <h1>Guess the Anime Release 📺</h1>
        <img src="{anime['image']}" width="300"><br><br>
        <h2>{anime['title']}</h2>

        <form method="POST">
            <input type="hidden" name="correct_year" value="{anime['year']}">
            <input type="hidden" name="correct_season" value="{anime['season']}">

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
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)