from flask import request, render_template, redirect, url_for
from flask_login import logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from PIL import Image
import os
import datetime

from db import *
from main import app, login_manager


@app.route("/admin_panel")
@login_required
def admin_panel():
    if current_user.id == 1 and current_user.login == 'admin':
        return render_template('admin_panel.html')
    return redirect('/authorization')


@app.route("/admin_panel/new_user", methods=['GET', 'POST'])
@login_required
def ap_new_user():
    if current_user.id == 1 and current_user.login == 'admin':
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            fio = request.form.get('fio')
            res = register(login, password, fio)
            if res == 0:
                return redirect('/admin_panel')
            elif res == 1:
                return render_template('ap_new_user.html', text='Пользователь уже существует')
            else:
                return render_template('ap_new_user.html')

        return render_template('ap_new_user.html')
    return redirect(url_for('authorization'))


@app.route('/admin_panel/delete_user')
def ap_delete_user():
    users = get_all_users()
    for user in users:
        user['path'] = '/admin_panel/delete_user_' + user['id']

    return render_template('ap_table_users.html', users=users)


@app.route('/admin_panel/delete_user_<int:n>')
def ap_du_work(n):
    res = delete_user(n)
    return redirect('/admin_panel')
