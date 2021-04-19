from dataclasses import asdict

from sanic.request import Request
from sanic.response import json
from sanic_jwt import protected
from sanic_restful import Resource

from src.db import poly_db
from src.definitions import BadRequestError, ApiError, PolyData, KeyVal


class PolyDataResource(Resource):
    decorators = [protected()]

    async def get(self, request: Request, object_id: int):
        result = poly_db.get(doc_id=object_id)

        if not result:
            raise ApiError(
                status_code=404,
                error_code="Not Found",
                message=f"Resource with id {object_id} was not found",
            )

        return json(asdict(PolyData(object_id=result.doc_id, data=result["data"])))

    async def delete(self, request: Request, object_id: int):
        try:
            _ = poly_db.remove(doc_ids=[object_id])
        except KeyError:
            pass
        return "", 204


class PolyDataResourceList(Resource):
    async def get(self, request: Request):
        results = poly_db.all()
        return json(
            [
                asdict(PolyData(object_id=result.doc_id, data=result["data"]))
                for result in results
            ]
        )

    async def post(self, request: Request):
        try:
            body = request.json
            values = [asdict(KeyVal(**value)) for value in body.get("data")]
            object_id = poly_db.insert({"data": values})
            return json({"id": object_id, "values": values})
        except Exception as e:
            raise BadRequestError(message=str(e))
