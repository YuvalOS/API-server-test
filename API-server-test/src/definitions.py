from dataclasses import dataclass, asdict

import typing


class ApiError(Exception):
    def __init__(
        self, status_code: int, error_code: str, message: str, *args: object
    ) -> None:
        super().__init__(*args)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


class BadRequestError(ApiError):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(400, error_code="BadRequest", message=message, *args)


class UnauthorizedError(ApiError):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(401, error_code="Unauthorized", message=message, *args)


@dataclass
class KeyVal:
    key: str
    val: typing.Any
    valType: str


@dataclass
class PolyData:
    object_id: int
    data: typing.List[KeyVal]


@dataclass
class User:
    username: str
    password: str

    def to_dict(self) -> dict:
        return asdict(self)
