from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


# -----------------------------------
# Get user by email
# -----------------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# -----------------------------------
# Create user
# -----------------------------------
def create_user(db: Session, user_in: UserCreate):
    # check existing user (important for race condition awareness)
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = get_password_hash(user_in.password)

    new_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role,
        password_hash=hashed_password,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user