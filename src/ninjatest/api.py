from ninja import NinjaAPI, Schema, ModelSchema
from django.http import HttpResponse
from ninja.operation import ResponseObject
from django.contrib.auth.models import User

class UserOut(Schema):
    """The schema with two str fields where one has a resolve_ method."""
    username: str
    foo: str

    def resolve_foo(self, obj):
        return "resolved foo"

api = NinjaAPI()

@api.get("/schema/returnmodel-works", response=UserOut)
def returnmodel_works(request):
    """Return a model instance directly, the foo field is resolved."""
    return User.objects.get_or_create(username="test")[0]

@api.get("/schema/returndict-broken", response=UserOut)
def returndict_broken(request):
    """Return a dict directly, the foo field is not resolved."""
    return {"username": "some user"}

@api.get("/schema/returndict-manual-schema", response=UserOut)
def returndict_manual_schema(request):
    """Use the UserOut schema manually, the foo field is resolved.
    Note that this fails when run in a debugger with breakpoints set."""
    schema = UserOut.from_orm({"username": "some user"})
    return HttpResponse(schema.json())