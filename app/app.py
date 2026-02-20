from flask import Flask, render_template_string
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return '<a href="/random-anime">Get random anime 🎌</a>'

@app.route("/random-anime")
def random_anime():
    url = "https://api.jikan.moe/v4/random/anime"
    response = requests.get(url)
    data = response.json()["data"]

    title = data["title"]
    synopsis = data["synopsis"]
    image = data["images"]["jpg"]["image_url"]
    link = data["url"]

    html = f"""
    <html>
        <body style="font-family: Arial; text-align:center; padding:40px;">
            <h1>{title}</h1>
            <img src="{image}" style="width:300px;"><br><br>
            <p style="max-width:600px; margin:auto;">{synopsis}</p>
            <br>
            <a href="{link}" target="_blank">View details</a><br><br>
            <a href="/random-anime">🔄 Another recommendation</a>
        </body>
    </html>
    """

    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)