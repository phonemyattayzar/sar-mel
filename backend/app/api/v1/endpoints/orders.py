from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User

from app.schemas.order import OrderCreate, OrderOut

from app.crud.crud_order import (
    create_order,
    get_orders_by_user,
)

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=OrderOut)
def checkout(
    order_in: OrderCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_order(db=db, order_in=order_in, user_id=current_user.id)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )



@router.get("/user/{user_id}", response_model=list[OrderOut])
def get_user_orders(
    user_id: UUID,
    db: Session = Depends(get_session),
):
    return get_orders_by_user(db=db, user_id=user_id)