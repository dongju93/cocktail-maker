from typing import Annotated, TypedDict

from pydantic import BaseModel, EmailStr, Field, field_validator


class User(BaseModel):
    user_id: Annotated[str, Field(..., min_length=4, max_length=14)]
    password: Annotated[str, Field(..., min_length=8, max_length=20)]
    email: Annotated[EmailStr, Field(...)]
    roles: Annotated[list[str], Field(..., min_items=1, max_items=4)]
    firstname: Annotated[str, Field(..., min_length=1, max_length=30)]
    lastname: Annotated[str, Field(..., min_length=1, max_length=30)]
    address: Annotated[str, Field(..., min_length=1, max_length=100)]
    phone_number: Annotated[str, Field(..., min_length=11, max_length=11)]

    @field_validator("user_id", "firstname", "lastname")
    @classmethod
    def user_id_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Field must be alphanumeric")
        return v

    @field_validator("phone_number")
    @classmethod
    def phone_number_numeric(cls, v):
        if not v.isnumeric():
            raise ValueError("Phone Number must be numeric")
        return v


class Login(BaseModel):
    user_id: Annotated[str, Field(..., min_length=4, max_length=14)]
    password: Annotated[str, Field(..., min_length=8, max_length=20)]

    @field_validator("user_id")
    @classmethod
    def user_id_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("user_id must be alphanumeric")
        return v


class PasswordAndSalt(TypedDict):
    encrypted_password: str
    salt: str
