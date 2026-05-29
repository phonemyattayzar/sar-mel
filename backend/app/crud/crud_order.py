import secrets
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.schemas.order import OrderCreate


def generate_order_number() -> str:
    # Note: If using SQLAlchemy 2.0+ or modern Python, consider datetime.now(timezone.utc)
    date_part = datetime.utcnow().strftime("%Y%m%d")
    random_part = secrets.token_hex(3).upper()
    return f"ORD-{date_part}-{random_part}"


def create_order(db: Session, order_in: OrderCreate, user_id: UUID):

    try:
        # 1. Gather all unique menu item IDs from the request
        menu_item_ids = list({item.menu_item_id for item in order_in.items})
        
        if not menu_item_ids:
            raise ValueError("Order must contain at least one item")

        # 2. BATCH QUERY: Fetch all required menu items in ONE shot
        menu_items = (
            db.query(MenuItem)
            .filter(MenuItem.id.in_(menu_item_ids))
            .all()
        )

        # 3. Create a lookup map for O(1) complexity inside the loop
        menu_item_map = {item.id: item for item in menu_items}

        total_amount = 0
        order_items_to_create = []

        # 4. Validate and calculate totals using the in-memory map
        for item in order_in.items:
            menu_item = menu_item_map.get(item.menu_item_id)
            
            if not menu_item:
                raise ValueError(f"Menu item with ID {item.menu_item_id} not found")

            item_total = menu_item.price_mmk * item.quantity
            total_amount += item_total

            order_items_to_create.append(
                {
                    "menu_item_id": menu_item.id,
                    "quantity": item.quantity,
                    "price_at_purchase": menu_item.price_mmk,
                }
            )

        # 5. Insert the parent Order record
        db_order = Order(
            user_id=user_id,
            restaurant_id=order_in.restaurant_id,
            delivery_address=order_in.delivery_address,
            order_number=generate_order_number(),
            total_amount_mmk=total_amount,
            order_status="pending",
        )

        db.add(db_order)
        db.flush()  # Flushes to DB to populate db_order.id

        # 6. Insert all OrderItems
        for item in order_items_to_create:
            db_order_item = OrderItem(
                order_id=db_order.id,
                menu_item_id=item["menu_item_id"],
                quantity=item["quantity"],
                price_at_purchase=item["price_at_purchase"],
            )
            db.add(db_order_item)

        db.commit()
        db.refresh(db_order)
        return db_order

    except Exception:
        db.rollback()
        raise


def get_orders_by_user(db: Session, user_id):
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )