from sqlite3.dbapi2 import Cursor
from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("movies.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


# movies_list = [
#     {
#         "id": 0,
#         "director": "Christopher Nolan",
#         "title": "Interstellar",
#         "genre": "Science-Fiction" 
#     },
#     {
#         "id": 1,
#         "director": "Martin Scorsese",
#         "title": "Shutter Island",
#         "genre": "Psychothriller"
#     },
#     {
#         "id": 2,
#         "director": "David Fincher",
#         "title": "Fight Club",
#         "genre": "Psychothriller"
#     },
#     {
#         "id": 3,
#         "director": "Hayao Miyazaki",
#         "title": "Spirited Away",
#         "genre": "Animated Fantasy Film"
#     },
#     {
#         "id": 4,
#         "director": "Scott Derrickson",
#         "title": "Doctor Strange",
#         "genre": "Superhero film"
#     }
# ]

#https://developer.mozilla.org/de/docs/Web/HTTP/Status
@app.route('/movies', methods=['GET', 'POST'])
def movies():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM movie")
        movies = [
            dict(id=row[0], director = row[1], genre = row[2], title = row[3])
            for row in cursor.fetchall()
        ]
        if movies is not None:
            return jsonify(movies), 200
        # if len(movies_list) > 0:
        #     return jsonify(movies_list)
        # else:
        #     # Mal eine Alternative zu 404(Not Found)
        #     'No Movies Found', 418
    if request.method == 'POST':
        new_director = request.form['director']
        new_genre = request.form['genre']
        new_title = request.form['title']
        # id = movies_list[-1]['id']+1
        sql = """INSERT INTO movie (director, genre, title)
                VALUES (?, ?, ?)"""
        # new_obj = {
        #     'id': id,
        #     'director': new_director,
        #     'genre': new_genre,
        #     'title': new_title
        # }
        cursor = cursor.execute(sql, (new_director, new_genre, new_title))
        conn.commit()

        return f"Book with the id: {cursor.lastrowid} created successfully", 201

        # movies_list.append(new_obj)
        # return jsonify(movies_list), 201

@app.route('/movie/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_movie(id):
    conn = db_connection()
    cursor = conn.cursor()
    movie = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM movie WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            movie = r
        if movie is not None:
            return jsonify(movie), 200
        else: 
            return "This movie does not exist", 404
        # for movie in movies_list:
        #     if movie['id'] == id:
        #         return jsonify(movie)
        #     pass
    if request.method == 'PUT':
        sql = """UPDATE movie
                SET director=?,
                    genre=?,
                    title=?
                WHERE id=? """
        #for movie in movies_list:
        #   if movie['id'] == id:
        director= request.form['director']
        genre = request.form['genre']
        title = request.form['title']
        updated_movie = {
            'id': id,
            'director': director,
            'genre': genre,
            'title': title        
        }
        conn.execute(sql, (director, genre, title, id))
        conn.commit()
        return jsonify(updated_movie)
    if request.method == 'DELETE':
        sql = """DELETE FROM movie WHERE id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        return "The movie with the ID: {} has been deleted.".format(id), 200
        # for index, movie in enumerate(movies_list):
        #     if movie['id'] == id:
        #         movies_list.pop(index)
        #         return jsonify(movies_list)



    
if __name__ == '__main__':
    # make app reachable on host when running in docker
    app.run(host='0.0.0.0')