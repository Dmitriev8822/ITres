from flask_login import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
