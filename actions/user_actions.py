import bcrypt
from database import SessionLocal

from models.user_model import UserModel
from interfaces.user import UserCreate


def get_user_by_email(email: str, db: SessionLocal):
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_id(id: int, db: SessionLocal) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == id).first()


def check_user_password(db: SessionLocal, email: str, password: str):
    db_user = get_user_by_email(email=email, db=db)
    if db_user:
        if bcrypt.checkpw(
            password.encode("utf8"), db_user.hashed_password.encode("utf8")
        ):
            return db_user
    return None


def create_user(db: SessionLocal, user: UserCreate) -> UserModel:
    try:
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf8"), salt=bcrypt.gensalt()
        )
        db_user = UserModel(
            email=user.email, hashed_password=hashed_password.decode("utf8")
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        return None
