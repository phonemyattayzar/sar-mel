from sqlalchemy.orm import Session
from uuid import UUID

from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate


def create_menu_item(db: Session, menu_item_in: MenuItemCreate) -> MenuItem:
    db_menu_item = MenuItem(
        name=menu_item_in.name,
        description=menu_item_in.description,
        price_mmk=menu_item_in.price_mmk,
        is_available=menu_item_in.is_available,
        preparation_time_minutes=menu_item_in.preparation_time_minutes,
        image_url=menu_item_in.image_url,
        restaurant_id=menu_item_in.restaurant_id,
        category_id=menu_item_in.category_id,
    )

    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item


def get_menu_items_by_restaurant(db: Session, restaurant_id: UUID) -> list[MenuItem]:
    return (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .all()
    )


def get_menu_items_by_category(db: Session, category_id: UUID) -> list[MenuItem]:
    return (
        db.query(MenuItem)
        .filter(MenuItem.category_id == category_id)
        .all()
    )
