from typing import Optional, List
import datetime
from pydantic import BaseModel, Field, field_validator
from constants import Roles, Location

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str = Field(min_length=1, max_length=20, description="passwordRepeat совпадает с полем password")
    passwordRepeat: str = Field(min_length=1, max_length=20, description="passwordRepeat совпадает с полем password")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    @field_validator("passwordRepeat")
    @classmethod
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value  # Преобразуем Enum в строку
        }

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")
    password: Optional[str] = None
    @field_validator("createdAt")
    @classmethod
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value


class OrderedMap(BaseModel):
    name: str


class ReviewUser(BaseModel):
    fullName: str


class Review(BaseModel):
    userId: str
    rating: float = Field(ge=0, le=5)
    text: str
    createdAt: datetime.datetime
    user: ReviewUser


class CreatedMoviesResponse(BaseModel):
    id: int = Field(ge=10000, le=999999, description="ID Фильма")
    name: str =  Field(min_length=3, max_length=100, description="Название Фильма")
    price: int = Field(ge=100, le=1000, description="Цена фильма")
    description: str
    imageUrl: str
    location: Location = Field(description="Локация")
    published: bool
    genreId: int
    genre: OrderedMap
    createdAt: datetime.datetime
    rating: float = Field(ge=0, le=5)


class MovieWithReviewsResponse(CreatedMoviesResponse):
    reviews: List[Review] = Field(default_factory=list, description="Отзывы")