from api import Resource, abort, reqparse, auth
from api.models.tag import TagModel
from api.schemas.tag import tag_schema, tags_schema, TagSchema, TagRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(description="API for tags", tags=['Tags'])
class TagResource(MethodResource):

    @marshal_with(TagSchema)
    @doc(summary="Get tag by ig")
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        return tag, 200

    @auth.login_required
    @use_kwargs(TagRequestSchema, location=('json'))
    @marshal_with(TagSchema, code=200)
    def put(self, tag_id, **kwargs):
        tag_data = TagModel(**kwargs)
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        tag.name = tag_data.name
        tag.save
        return tag, 200

    @auth.login_required
    @marshal_with(TagSchema, code=200)
    def delete(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"tag {tag_id} not found")
        tag.delete()
        return tag, 200


@doc(description="API for tags", tags=["Tags"])
class TagsListResource(MethodResource):

    @marshal_with(TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    # @use_kwargs(TagRequestSchema, location=('json'))  # можно так, но лучше:
    @use_kwargs({"name": fields.Str(required=True)})        # наглядно, если не нужно много параметров
    @marshal_with(TagSchema, code=201)
    @doc(summary="Create new tag")
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        if not tag.id:
            abort(400, error=f"Tag with name {tag.name} already exists")
        return tag, 201
