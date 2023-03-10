from flask_restx import Namespace, Resource
from flask import request
from models import MovieSchema, Movie
from setup_db import db

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year_id = request.args.get('year')
        mov_query = db.session.query(Movie)
        if director_id:
            mov_query = mov_query.filter(director_id == Movie.director_id)
        if genre_id:
            mov_query = mov_query.filter(genre_id == Movie.genre_id)
        if year_id:
            mov_query = mov_query.filter(year_id == Movie.year)
        movies = mov_query.all()
        return MovieSchema(many=True).dump(movies), 200

    def post(self):
        movie_add = Movie(**request.json)

        db.session.add(movie_add)
        db.session.commit()
        return "", 201


@movie_ns.route('/<int:uid>')
class MoviesView(Resource):
    def get(self, uid: int):
        movie = Movie.query.get(uid)
        if not movie:
            return 'NOT FOUND', 404
        return MovieSchema().dump(movie), 200

    def put(self, uid: int):
        movie = db.session.query(Movie).get(uid)
        movie.title = request.json.get("title")
        movie.description = request.json.get("description")
        movie.trailer = request.json.get("trailer")
        movie.year = request.json.get("year")
        movie.rating = request.json.get("rating")
        movie.genre_id = request.json.get("genre_id")
        movie.director_id = request.json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 201

    def delete(self, uid: int):
        db.session.delete(db.session.query(Movie).get(uid))
        db.session.commit()
        return "", 204
