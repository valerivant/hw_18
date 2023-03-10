from flask_restx import Namespace, Resource

from models import DirectorSchema, Director
from setup_db import db



director_ns = Namespace('directors')

@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        return DirectorSchema(many=True).dump(directors), 200


@director_ns.route('/<int:dirid>')
class DirectorView(Resource):
    def get(self, dirid: int):
        director = db.session.query(Director).get(dirid)
        if not director:
            return 'NOT FOUND', 404
        return DirectorSchema().dump(director), 200




