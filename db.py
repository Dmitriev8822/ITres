from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash, generate_password_hash

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
    date = db.Column(db.String(20), nullable=False)


def create_db():
    db.create_all()


def check_user(login, password):
    user = User.query.filter_by(login=login).first()
    if user is None:
        return 1  # user not found

    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return 0  # all ok
        else:
            return 3  # password incorrect


def register(login, password, fio):
    existing_user = User.query.filter_by(login=login).first()
    if existing_user:
        return 1  # user existing

    hashed_password = generate_password_hash(password)

    new_user = User(login=login, password=hashed_password, fio=fio)
    db.session.add(new_user)
    db.session.commit()

    return 0  # all ok


def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return 1  # user not found

    db.session.delete(user)
    db.session.commit()

    return 0


def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': str(user.id),
            'login': user.login,
            'fio': user.fio
        })
    return result


def new_news(user, title, text, date):
    news = Article(user=user, title=title, text=text, date=date)

    db.session.add(news)
    db.session.commit()

    return news.id  # all ok


def get_all_news():
    all_news = Article.query.all()
    result = []
    for news in all_news:
        result.append({
            'id': str(news.id),
            'title': news.title,
            'text': news.text,
            'date': news.date
        })
    return result


def get_news(id):
    news = Article.query.filter_by(id=id).first()
    result = {
        'id': str(news.id),
        'title': news.title,
        'text': news.text,
        'date': news.date
    }
    return result


def get_personal_news(id):
    all_news = Article.query.filter_by(user=id).all()
    result = list()
    for news in all_news:
        result.append({
            'id': str(news.id),
            'title': news.title,
            'text': news.text,
            'date': news.date
        })
    return result


def news_add():
    new_news(user='1', title='Breaking News: Major Earthquake Hits Coastal City',
             text='A powerful earthquake measuring 7.8 on the Richter scale struck a coastal city earlier today. The tremors were felt throughout the region, causing widespread panic and damage to buildings. Rescue teams have been dispatched to the affected areas to assess the situation and provide assistance to those in need.')

    new_news(user='2', title='Scientists Make Breakthrough in Cancer Research',
             text='In a groundbreaking development, scientists have discovered a new treatment that shows promising results in combating certain types of cancer. The experimental therapy has been tested on mice and has shown significant tumor regression without causing harmful side effects. Researchers are hopeful that this breakthrough will lead to more effective treatments for cancer patients in the future.')

    new_news(user='3', title='Space Exploration Update: New Exoplanet Discovered',
             text='Astronomers have detected a potentially habitable exoplanet located within the habitable zone of a distant star system. The newly discovered planet, named Proxima C, has similar characteristics to Earth and may have the necessary conditions to support life. The finding has sparked excitement among scientists and renewed interest in the search for extraterrestrial life.')

    new_news(user='1', title='Tech Giant Unveils Next-Generation Smartphone',
             text='Leading technology company XYZ has announced the launch of their highly anticipated smartphone, featuring cutting-edge specifications and innovative features. The new device boasts a faster processor, improved camera capabilities, and enhanced security features. Tech enthusiasts are eagerly waiting to get their hands on the latest offering from XYZ.')

    new_news(user='5', title='Sports Update: Team X Wins Championship',
             text='In a thrilling match that went down to the wire, Team X emerged victorious in the championship final. The team showcased exceptional skill and teamwork to secure their victory, defeating their opponents by a narrow margin. Celebrations are underway as fans and players alike rejoice in this historic win.')

    new_news(user='2', title='Health & Wellness: Importance of Regular Exercise',
             text='Experts emphasize the importance of incorporating regular exercise into our daily routines. Physical activity not only helps maintain a healthy weight but also reduces the risk of various chronic conditions, including heart disease, diabetes, and certain types of cancer. It is recommended to engage in at least 150 minutes of moderate-intensity aerobic activity per week.')

    new_news(user='1', title='Environmental News: Climate Change Awareness Campaign',
             text='In an effort to combat climate change, a global awareness campaign has been launched to highlight the urgency of the issue and encourage individuals and organizations to take action. The campaign aims to raise awareness about the impact of climate change on the planet and inspire sustainable practices to mitigate its effects.')

    new_news(user='2', title='Financial Update: Stock Market Hits Record High',
             text='The stock market reached a new all-time high, driven by positive economic indicators and investor optimism. Several key sectors, including technology, healthcare, and renewable energy, have experienced significant gains. Analysts predict that the strong performance of the market will continue in the coming months.')

    new_news(user='5', title='Arts & Culture: New Exhibition at Local Museum',
             text='A local museum is opening a new exhibition showcasing works by renowned artists from around the world. The exhibition features a diverse collection of paintings, sculptures, and multimedia installations, offering visitors a unique cultural experience. Art enthusiasts are eagerly anticipating the opening.')

    new_news(user='1', title='Travel Update: Top Destinations for Summer Vacation',
             text='As summer approaches, travel enthusiasts are planning their vacations to popular destinations. Some of the top choices for this year include tropical beach resorts, European cities with rich history and culture, and scenic mountain getaways. Travel agencies and airlines are offering attractive deals to cater to the increased demand.')


def create_admin():
    register(login='admin', password='TyB7L4hL$#Wx', fio='')


if __name__ == '__main__':
    create_db()
    create_admin()
