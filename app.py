from flask import Flask, render_template, request
import requests

app = Flask(__name__)

PROXY_URL = "https://thingproxy.freeboard.io/fetch/"

def search_anime(query):
    api_url = f"https://anime-api-taupe.vercel.app/aniwatch/search?keyword={query}&page=1"
    proxied_url = f"{PROXY_URL}{api_url}"
    try:
        response = requests.get(proxied_url)
        response.raise_for_status()
        data = response.json()
        animes = data.get("animes")
        if animes and len(animes) > 0:
            for a in animes:
                a['title'] = a.get('title') or a.get('name') or 'Sem título'
                a['image'] = a.get('image') or a.get('img') or ''
                a['id'] = a.get('id') or ''
            return animes
        else:
            popular = data.get("mostPopularAnimes", [])
            for a in popular:
                a['title'] = a.get('name') or 'Sem título'
                a['image'] = a.get('img') or ''
                a['id'] = a.get('id') or ''
            return popular
    except Exception as e:
        print(f"Erro na busca: {e}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            results = search_anime(query)
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)



