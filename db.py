import sqlite3

conn = sqlite3.connect("movies.sqlite")

cursor = conn.cursor()
sql_query = """CREATE TABLE movie (
    id integer PRIMARY KEY,
    director text NOT NULL,
    genre text NOT NULL,
    title text NOT NULL
)"""
cursor.execute(sql_query)