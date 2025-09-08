from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from argon2.exceptions import VerificationError


from database import get_db
from domain.data_extract import de_schema
from domain.data_extract import de_crud

router = APIRouter(
    prefix="/api/db",
)


@router.get("/user/all", response_model=de_schema.UserdbList)
def user_db_list(db: Session = Depends(get_db)):
    List=de_crud.user_db_list(db)
    #print("!!!!")
    #print(List)
    return {"dblist":List}
    
@router.get("/record/all", response_model=de_schema.RecorddbList)
def record_db_list(db: Session = Depends(get_db)):
    List=de_crud.record_db_list(db)
    return {"dblist":List}
    
@router.get("/detail/all", response_model=de_schema.DetaildbList)
def detail_db_list(db: Session = Depends(get_db)):
    List=de_crud.detail_db_list(db)
    return {"dblist":List}
    
@router.get("/detail/cnt", response_model=de_schema.DetaildbList)
def detail_db_list(offset : int = 0, limit : int = 0, db: Session = Depends(get_db)):
    List=de_crud.detail_db_list_cnt(offset,limit,db)
    return {"dblist":List}
    