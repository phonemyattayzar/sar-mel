from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.menu_item import MenuItemCreate, MenuItemOut
from app.schemas.category import CategoryWithMenuItems
from app.crud.crud_menu_item import (
    create_menu_item,
    get_menu_items_by_restaurant,
    get_menu_items_by_category,
)
from app.crud.crud_restaurant import get_restaurant
from app.crud.crud_category import get_categories_by_restaurant
from app.models.category import Category

router = APIRouter(prefix="/menu-items", tags=["menu-items"])


@router.post(
    "/",
    response_model=MenuItemOut,
    status_code=status.HTTP_201_CREATED,
)
def create_new_menu_item(
    menu_item_in: MenuItemCreate,
    db: Session = Depends(get_session),
):
    # 1. Verify restaurant exists
    restaurant = get_restaurant(db=db, restaurant_id=menu_item_in.restaurant_id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    # 2. If category_id is provided, verify it exists and belongs to the restaurant
    if menu_item_in.category_id:
        category = (
            db.query(Category)
            .filter(Category.id == menu_item_in.category_id)
            .first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        if category.restaurant_id != menu_item_in.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not belong to the specified restaurant",
            )

    return create_menu_item(db=db, menu_item_in=menu_item_in)


@router.get(
    "/restaurant/{restaurant_id}",
    response_model=list[MenuItemOut],
)
def list_menu_items_by_restaurant(
    restaurant_id: UUID,
    db: Session = Depends(get_session),
):
    # Verify restaurant exists
    restaurant = get_restaurant(db=db, restaurant_id=restaurant_id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    return get_menu_items_by_restaurant(db=db, restaurant_id=restaurant_id)


@router.get(
    "/category/{category_id}",
    response_model=list[MenuItemOut],
)
def list_menu_items_by_category(
    category_id: UUID,
    db: Session = Depends(get_session),
):
    # Verify category exists
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return get_menu_items_by_category(db=db, category_id=category_id)


@router.get(
    "/restaurant/{restaurant_id}/menu",
    response_model=list[CategoryWithMenuItems],
)
def get_restaurant_menu(
    restaurant_id: UUID,
    db: Session = Depends(get_session),
):
    # Verify restaurant exists
    restaurant = get_restaurant(db=db, restaurant_id=restaurant_id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    # Fetch all categories for this restaurant
    categories = get_categories_by_restaurant(db=db, restaurant_id=restaurant_id)
    return categories
