from flask_restful import marshal_with
from api import auth, abort, g, Resource, reqparse
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.note import note_schema, notes_schema, NoteSchema, NoteRequestSchema
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from webargs import fields


@doc(tags=["Notes"])
class NoteResource(MethodResource):
    @auth.login_required
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        return note_schema.dump(note), 200

    @auth.login_required
    def put(self, note_id):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)
        note_data = parser.parse_args()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = note_data["text"]
        if note_data.get('private') is not None:
            note.private = note_data.get("private")

        note.save()
        return note_schema.dump(note), 200

    @auth.login_required
    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.delete()
        # raise NotImplemented("Метод не реализован")
        return note_schema.dump(note), 200


@doc(tags=["Notes"])
class NotesListResource(MethodResource):
    def get(self):
        notes = NoteModel.query.all()
        return notes_schema.dump(notes), 200

    @doc(summary="Create Note", description="Create new Note for current authentication")
    @doc(security=[{"basicAuth": []}])
    @marshal_with(NoteSchema, code=201)
    @doc(responses={400: {"description": 'bad request'}})
    @use_kwargs(NoteRequestSchema, location="json")
    @auth.login_required
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=["Notes"])
class NotesAddTagResource(MethodResource):

    @doc(summary="Add tags to note")
    @use_kwargs({"tags": fields.List(fields.Int())})
    def put(self, note_id, **kwargs):
        # print("kwargs = ", kwargs)
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        # TagModel.query.filter(TagModel.id.in_(kwargs["tags"])).all()      # ЛУЧШЕ ТАК!!!

        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)        #работает медленно... Лучше получить сразу список
            note.tags.append(tag)

        note.save()
        return {}


@doc(tags=["Notes"])
class NotesFilterResource(MethodResource):
    # GET: /notes/filter?tags=[tag-1, tag-2, ...]
    @use_kwargs({"tags": fields.List(fields.Str())}, location=("query"))
    def get(self, **kwargs):
        pass