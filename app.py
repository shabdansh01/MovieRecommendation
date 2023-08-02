from flask import Flask, render_template, request
import pickle
import pandas as pd
import difflib
import requests

app = Flask(__name__)
df = pickle.load(open('movies.pkl', 'rb'))
title_list = pickle.load(open('title_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    path = response.json()
    return  'https://image.tmdb.org/t/p/w500/' + path['poster_path']

@app.route('/', methods=['GET', 'POST'])
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    user_input = str(request.form.get('user_input'))
    try:
        movie_index = df[df['title'] == user_input].index[0]
    except:
        close_match = difflib.get_close_matches(user_input, title_list)
        # print(close_match)
        movie_index = df[df['title'] == close_match[0]].index[0]
    finally:
        try:
            distance = similarity[movie_index]
        except:
            distance = similarity[679]
        movies_list = sorted(list(enumerate(distance)), key = lambda x: x[1], reverse= True)[1:6]
        # print(movies_list[0])

        data = []   
        poster = []
        for i in movies_list:
            movie_id = df.iloc[i[0]]['movie_id']
            poster.append(fetch_poster(movie_id))
            data.append(df.iloc[i[0]]['title'])
        return render_template('recommend.html', data = data, poster = poster)



if __name__ == '__main__':
    app.run(debug=True)
