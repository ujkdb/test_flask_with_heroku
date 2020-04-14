import flask
import os
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, IntegerField, SubmitField
# from werkzeug import secure_filename
from wtforms.validators import DataRequired
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.users import User
from data.news import News

from api import news_api
from api_v2.news_resource import NewsResource
from api_v2.news_list_resource import NewsListResource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    users = session.query(User).all()
    return render_template('index.html', users=users, last_news=flask.session.get("last_news", ""))


@app.route('/news')
def news():
    session = db_session.create_session()
    news = [(news_.content, news_.user_id) for news_ in session.query(News).all()]
    print(news)
    return render_template('news.html', news=news)


class AddNewsForm(FlaskForm):
    user = IntegerField("ID автора", validators=[DataRequired()])
    content = StringField("Новость", validators=[DataRequired()])
    submit = SubmitField("Загрузить")


@app.route('/addnews', methods=['GET', 'POST'])
def add_news():
    form = AddNewsForm()
    if form.validate_on_submit():
        news_ = News()
        news_.user_id = form.user.data
        news_.title = "Title"
        news_.content = form.content.data
        session = db_session.create_session()
        session.add(news_)
        session.commit()
        flask.session["last_news"] = news_.content
        return redirect("/news")
    return render_template('addnews.html', form=form)


class AvatarForm(FlaskForm):
    file = FileField("Файл", validators=[DataRequired()])
    submit = SubmitField("Загрузить")


@app.route('/avatar', methods=['GET', 'POST'])
def avatar():
    form = AvatarForm()
    if form.validate_on_submit():
        avatar_path = f'static/img/ava_{form.file.data.filename}'  # secure_filename(form.file.data.filename)
        form.file.data.save(avatar_path)
        return render_template('avatar.html', form=form, avatar=avatar_path)
    return render_template('avatar.html', form=form)


api.add_resource(NewsResource, '/api/v2/news/<int:news_id>')
api.add_resource(NewsListResource, '/api/v2/news')

if __name__ == '__main__':
    db_session.global_init("db/test.sqlite")
    app.register_blueprint(news_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
