from flask_restx import Namespace, Resource
from flask import request
from models import GenreSchema, Genre
from setup_db import db


genre_ns = Namespace('genres')

@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return GenreSchema(many=True).dump(genres), 200


@genre_ns.route('/<int:genid>')
class GenreView(Resource):
    def get(self, genid: int):
        genre = db.session.query(Genre).get(genid)
        if not genre:
            return 'NOT FOUND', 404
        return GenreSchema().dump(genre), 200