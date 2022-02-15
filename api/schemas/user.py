from api import ma
from api.models.user import UserModel


#       schema        flask-restful
# object ------>  dict ----------> json

# json ----> dict
# Сериализация ответа(response)
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'is_staff', 'role')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('userresource', values=dict(user_id="<id>")),
        'collection': ma.URLFor('userslistresource')
    })


# Десериализация запроса(request)
class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.Str()
    password = ma.Str()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
