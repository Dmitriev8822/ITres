from flask_login import UserMixin, login_user
from main import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fio = db.Column(db.String(100), nullable=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)


def create_db():
    db.create_all()


def check_user(login, password):
    user = User.query.filter_by(login=login).first()
    if user is None:
        return 1  # user not found

    if user:
        if user.password == password:
            login_user(user)
            return 0  # all ok
        else:
            return 3  # password incorrect


def register(login, password, fio):
    existing_user = User.query.filter_by(login=login).first()
    if existing_user:
        return 1  # user existing

    new_user = User(login=login, password=password, fio=fio, efficiency=0)
    db.session.add(new_user)
    db.session.commit()

    return 0  # all ok


def new_news(user, title, text):
    news = Article(user=user, title=title, text=text)
    cur_user = User.query.filter_by(id=user).first()
    cur_user.efficiency = cur_user.efficiency + 1

    db.session.add(news)
    db.session.commit()

    return 0  # all ok


if __name__ == '__main__':
    db.create_all()
