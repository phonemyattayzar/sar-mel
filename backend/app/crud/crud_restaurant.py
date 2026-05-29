from sqlalchemy.orm import Session
from uuid import UUID

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate


def get_restaurant(db: Session, restaurant_id: UUID):
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def get_multi_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Restaurant)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_restaurant(db: Session, restaurant_in: RestaurantCreate):
    db_restaurant = Restaurant(
        owner_id=restaurant_in.owner_id,
        name=restaurant_in.name,
        description=restaurant_in.description,
        phone_number=restaurant_in.phone_number,
        address=restaurant_in.address,
        township=restaurant_in.township,
        is_open=restaurant_in.is_open,
    )

    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant