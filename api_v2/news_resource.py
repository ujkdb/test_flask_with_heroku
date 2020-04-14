from flask_restful import Resource
from flask import jsonify

from data import db_session
from data.news import News


class NewsResource(Resource):
    def get(self, news_id):
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        print(news)
        return jsonify(
            {'news': [{'content': news.content, 'user_id': news.user_id}]})
