"""Schemas for authentication."""
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Form


class Token(BaseModel):
    """Response for login to access token endpoint."""
    access_token: str = Field(...,
                              example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                      "eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjI0NT"
                                      "YzMDAzfQ.SXuWTMZ0XvxCJN5uGt6ktQL59V5HrP"
                                      "jPZYu7tr6n9GY")
    token_type: str = Field("Bearer",
                            description="Type of the token.",
                            example="Bearer")


class AuthUserPublic(BaseModel):
    """Response for read_users_me endpoint."""
    username: str = Field(..., example="johndoe")
    email: Optional[str] = Field(None, example="john.doe@example.com")
    fullname: Optional[str] = Field(None, example="John Doe")
    is_active: Optional[bool] = Field(True, example="true")
    is_superuser: Optional[bool] = Field(False, example="false")


class LoginForm(BaseModel):
    """Request form for login to getting tokens."""
    username: str = Field(..., description="Username", example="johndoe")
    password: str = Field(..., description="Password in plaintext",
                          example="secret")

    def __init__(self,
                 username: str = Form(...),
                 password: str = Form(...)):
        super().__init__(username=username, password=password)


class AuthUserCreationForm(BaseModel):
    """Request form for creating a new user."""
    username: str = Field(..., description="Username", example="johndoe")
    fullname: str = Field(None, description="Full name", example="John Doe")
    password: str = Field(..., description="Password in plaintext",
                          example="secret")
    email: str = Field(None, description="Email address",
                       example="john.doe@example.com")
    is_superuser: bool = Field(False, description="Is it a superuser account",
                               example="false")

    def __init__(self,
                 username: str = Form(...),
                 fullname: str = Form(None),
                 password: str = Form(...),
                 email: str = Form(None),
                 is_superuser: bool = Form(False)):
        super().__init__(username=username, fullname=fullname,
                         password=password, email=email,
                         is_superuser=is_superuser)
