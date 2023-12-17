from flask import request, render_template, redirect
from flask_login import logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from PIL import Image
import os

from db import *
from main import app, login_manager

path_join_sing = '/'
path_to_news_images = path_join_sing.join(['static', 'images', 'news'])
path_to_temp_images = path_join_sing.join(['static', 'images', 'temp'])
path_to_serv_images = path_join_sing.join(['static', 'images', 'serv'])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        res = check_user(login, password)
        if res == 0:
            return redirect('/editor')
        elif res == 1:
            return render_template('login.html', login_text='Пользователь не найден')
        elif res == 3:
            return render_template('login.html', login_text="Некорректный пароль")
        else:
            return render_template('login.html')

    return render_template('login.html')


def is_image(name, folder, change=False, path=False):
    files = os.listdir(folder)
    for file in files:
        if file == name + '.jpg':
            file_n = file.split('.')[-2] + 'n.jpg'
            if path:
                return [path_join_sing.join([folder, file]), path_join_sing.join([folder, file_n])]

            if change:
                os.remove(path_join_sing.join([folder, file]))
                os.remove(path_join_sing.join([folder, file_n]))

            return True
    return False


def save_photo(file, image_path, name, max_size=720):
    image = Image.open(file)

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    width, height = image.size
    aspect_ratio = width / height

    if width > height:
        new_width = max_size
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max_size
        new_width = int(new_height * aspect_ratio)

    resized_image = image.resize((new_width, new_height))

    is_image(name, image_path, change=True)

    path_to_save = os.path.join(image_path, name) + '.jpg'
    resized_image.save(path_to_save)

    # resize image for news

    image = Image.open(path_to_save)

    width, height = image.size

    left = (width - 280) // 2
    upper = (height - 350) // 2
    right = left + 280
    lower = upper + 350

    cropped_image = image.crop((left, upper, right, lower))

    path_to_save = os.path.join(image_path, name + 'n') + '.jpg'
    cropped_image.save(path_to_save)


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('editor')
        photo = request.files.get('photo')
        photo.filename = secure_filename(photo.filename)

        art_id = new_news(user=str(current_user.id), title=title, text=text)

        save_photo(photo, path_to_news_images, str(art_id))
        return redirect('/all_news')

    return redirect('/editor')


# @app.route('/news_preview')
# def news_preview():
#     res = get_news()
#     for news in res:
#         news['photo'] = path_join_sing.join([r'..', path_to_news_images, news['id'] + '.jpg'])
#
#     # {'id': '4', 'title': '123', 'text': 'asdf', 'photo': '../static/images/news/4.jpg'}
#
#     return render_template('news_preview.html', all_news=res)

@app.route('/news_<int:n>')
def news(n):
    res = get_news(n)
    path_to_image = path_join_sing.join([path_to_news_images, res['id'] + '.jpg'])
    return render_template('news.html', title=res['title'], text=res['text'], image=path_to_image)


@app.route('/all_news')
def all_news():
    res = get_all_news()
    for news in res:
        if len(news['title']) > 15:
            news['title'] = news['title'][0:15] + '...'
        if len(news['text']) >= 25:
            news['text'] = news['text'][0:60] + '...'

        news['photo'] = path_join_sing.join([r'..', path_to_news_images, news['id'] + 'n.jpg'])

    return render_template('all_news.html', all_news=res)


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    return render_template('editor.html')


if __name__ == '__main__':
    create_db()
    register('123', '123', '312')
    app.run()
