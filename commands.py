import json
from sqlite3 import IntegrityError

import click
from api import app, db
from api.models.user import UserModel
from api.models.note import NoteModel
from api.schemas.user import UserRequestSchema
from config import BASE_DIR


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


@app.cli.command('add-list')
def listusers():
    """
    add list users from practice
    """
    users = [
        {"id": 1, "username": "SuperMan"},
        {"id": 2, "username": "Megaman"},
        {"id": 3, "username": "Admin"},
        {"id": 6, "username": "spiderman"},
        {"id": 8, "username": "User"},
        {"id": 9, "username": "NewUser"},
    ]
    for u in users:
        user = UserModel(u["username"], u["username"])
        user.id = u["id"]
        user.save()


@app.cli.command('fixture')
@click.argument('param')
def fixtures(param):
    path_to_fixture = BASE_DIR / 'fixtures' / 'notes.json'
    with open(path_to_fixture, "r", encoding="UTF-8") as f:
        models = {
            "NoteModel": NoteModel,
            "UserModel": UserModel
        }
        file_data = json.load(f)
        model_name = file_data["model"]
        for obj_data in file_data["records"]:
            obj = models[model_name](**obj_data)
            db.session.add(obj)
        db.session.commit()
    #     users_data = UserRequestSchema(many=True).loads(f.read())
    #     for user_data in users_data:
    #         user = UserModel(**user_data)
    #         db.session.add(user)
    #         try:
    #             db.session.commit()
    #         except IntegrityError:
    #             db.session.rollback()
    #             print(f'User {user.username} already exists')
    #     db.session.commit()
    # print(f"{len(users_data)} users created")
