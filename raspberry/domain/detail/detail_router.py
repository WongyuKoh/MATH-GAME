from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from argon2.exceptions import VerificationError


from database import get_db
from domain.detail import detail_crud
from domain.record import record_schema

# https://velog.io/@munang/Python-FastAPI-%EC%9D%98%EC%A1%B4%EC%84%B1-%EC%A3%BC%EC%9E%85-Depends-%ED%95%A8%EC%88%98
# Depends 함수는 그 안에 있는 값을 먼저 실행함


router = APIRouter(
    prefix="/api",
)


@router.get("/detail/{record_id}", response_model=record_schema.Record)
def record_detail_list(db: Session = Depends(get_db),
                  record_id=1):
    _user_list = detail_crud.get_detail_list(db,record_id=record_id)
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return _user_list
    
