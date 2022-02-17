import click
from api import app, db
from api.models.user import UserModel


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:") or "admin"  # лучше так, чем следующая строка
    # username = 'admin' if username == "" else username
    password = input("Password[default 'admin']:") or "admin"
    # password = 'admin' if password == "" else password
    user = UserModel(username, password, role="admin", is_staff=True)
    user.save()
    if user.id is None:
        print(f"User with username:{user.username} already exist")
    else:
        print(f"Superuser create successful! id={user.id}")


@app.cli.command('getallusers')
def get_all_users():
    """
    Print all users from database
    """
    users = UserModel.query.all()
    counter = 1
    # for u in users:
    #     print(f"{counter}. User id: {u.id} {u.username}\n")
    #     counter += 1
    for num, user in enumerate(users, 1):
        print(f"{num}. User id: {user.id} {user.username}")


@app.cli.command('remove-user')
@click.argument('username', default="")
@click.option('--all', default=False, is_flag=True)
def remove_user(username, all):
    """
    Remove user with UserName
    """
    if all:
        UserModel.query.delete()
        db.session.commit()
        return
    user = UserModel.query.filter_by(username=username).first()
    if user is None:
        print(f"User with name={username} not found")
        return
    UserModel.delete(user)
    print(f"User with name={username} successfully deleted")
