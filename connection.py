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
            if path:
                return path_join_sing.join([folder, file])

            if change:
                os.remove(path_join_sing.join([folder, file]))

            return True
    return False


def save_photo(file, image_path, name, max_size=720):
    path_to_save = os.path.join(image_path, name) + '.jpg'
    image = Image.open(file)

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
    resized_image.save(path_to_save)


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('editor')
        photo = request.files.get('photo')
        photo.filename = secure_filename(photo.filename)

        art_id = new_news(user=str(current_user.id), title=title, text=text)

        save_photo(photo, path_to_news_images, str(art_id))
        return redirect('/')

    return redirect('/editor')


@app.route('/news_preview')
def news_preview():
    res = get_news()
    for news in res:
        news['photo'] = path_join_sing.join([r'..', path_to_news_images, news['id'] + '.jpg'])

    print(res)

    return render_template('news_preview.html', all_news=res)


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    return render_template('editor.html')


if __name__ == '__main__':
    app.run()
