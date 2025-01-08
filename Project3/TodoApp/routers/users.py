
from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import Users
from database import SessionLocal

# from .auth import get_current_user ## -> Relative import
from routers.auth import get_current_user ## -> Absolute import

from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db ## return all info then run finally clause
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)] ## Simplifies type hinting and dependency declarations
user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=4)


@router.get("/current",status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="Authorization Failed")
    return  db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/change_password/",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=404,detail="Password not match")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()
