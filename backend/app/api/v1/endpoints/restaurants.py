from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.restaurant import RestaurantCreate, RestaurantOut
from app.crud.crud_restaurant import (
    create_restaurant,
    get_multi_restaurants,
    get_restaurant,
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.post(
    "/",
    response_model=RestaurantOut,
    status_code=status.HTTP_201_CREATED,
)
def create_new_restaurant(
    restaurant_in: RestaurantCreate,
    db: Session = Depends(get_session),
):
    return create_restaurant(db=db, restaurant_in=restaurant_in)


@router.get(
    "/",
    response_model=list[RestaurantOut],
)
def list_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
):
    return get_multi_restaurants(db=db, skip=skip, limit=limit)


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantOut,
)
def get_restaurant_detail(
    restaurant_id: UUID,
    db: Session = Depends(get_session),
):
    restaurant = get_restaurant(db=db, restaurant_id=restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return restaurant