import flask
from flask import jsonify
from data import db_session
from data.news import News

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/news')
def get_news():
    session = db_session.create_session()
    news = session.query(News).all()
    return jsonify(
        {
            'news':
                [{'content': item.content, 'user_id': item.user_id} for item in news]
        }
    )