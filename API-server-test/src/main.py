from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic_jwt import initialize
from sanic_restful import Api

from src.auth import authenticate
from src.definitions import ApiError, BadRequestError
from src.resources import PolyDataResource, PolyDataResourceList

app = Sanic("Polyrize Interview Server")
api = Api(app)
initialize(app, authenticate=authenticate, url_prefix="/api/auth")


def build_error_response(message, status_code, error_code, **kwargs):
    return json({"error": error_code, "message": message, **kwargs}, status=status_code)


# Handle exceptions
@app.exception(Exception)
def handle_error(request: Request, e):
    if isinstance(e, ApiError):
        return build_error_response(
            message=e.message, status_code=e.status_code, error_code=e.error_code
        )
    return build_error_response(
        message=str(e), status_code=500, error_code="Internal Server Error"
    )


@app.middleware("request")
async def check_headers(request):
    headers = request.headers
    try:
        content_type_ = headers["content-type"]
        if content_type_ != "application/json":
            raise BadRequestError("Content-Type must be application json")
    except KeyError:
        raise BadRequestError("Content-Type headers is required")


api.add_resource(PolyDataResourceList, "/api/poly")
api.add_resource(PolyDataResource, "/api/poly/<object_id:int>")
