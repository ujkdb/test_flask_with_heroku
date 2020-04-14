import flask
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.news import News

class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return flask.jsonify({'news': [{'content': item.content, 'user.name':item.user_id} for item in news]})