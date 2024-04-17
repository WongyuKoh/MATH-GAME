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

# https://velog.io/@munang/Python-FastAPI-%EC%9D%98%EC%A1%B4%EC%84%B1-%EC%A3%BC%EC%9E%85-Depends-%ED%95%A8%EC%88%98
# Depends 함수는 그 안에 있는 값을 먼저 실행함


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
    
