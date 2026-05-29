from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class RestaurantBase(BaseModel):
    name: str
    description: str | None = None
    phone_number: str
    address: str
    township: str
    is_open: bool = True

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not value.startswith("09"):
            raise ValueError("Phone number must start with 09")

        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(value) < 7 or len(value) > 15:
            raise ValueError("Invalid phone number length")

        return value


class RestaurantCreate(RestaurantBase):
    owner_id: UUID


class RestaurantOut(RestaurantBase):
    id: UUID
    owner_id: UUID
    logo_url: str | None = None
    cover_image_url: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)