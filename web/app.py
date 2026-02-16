
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_URL_ADD = 'http://localhost:8000/films/add'
API_URL_ALL = "http://localhost:8000/films/"

@app.route('/add', methods=['GET', 'POST'])
def add_new_film():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        release_year = request.form['release_year']
        genre = request.form['genre']
        rating = request.form['rating']

        payload = {
            'title': title,
            'director': director,
            'release_year': release_year,
            'genre': genre,
            'rating': rating
        }
        response = requests.post(API_URL_ADD, json=payload)
        if response.ok:
            return redirect(url_for('get_all_films'))
        else:
            return "An error occured. Check that you're not duplicating PK"
    return render_template('form.html')


@app.route('/')
def get_all_films():
    response = requests.get(API_URL_ALL)
    if response.ok:
        films = response.json()
        return render_template('films.html', films=films)
    else:
        return f"Failed to retrieve data. Status code: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')