from api import ma
from api.models.tag import TagModel


# Сериализация ответа(response)
class TagSchema(ma.SQLAlchemyAutoSchema):
    class Mets:
        model = TagModel
        fields = ('id', 'name')


# Десериализация запроса(request)
class TagRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    name = ma.Str()


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
