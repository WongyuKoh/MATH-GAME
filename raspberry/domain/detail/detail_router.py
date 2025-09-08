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

router = APIRouter(
    prefix="/api",
)


@router.get("/detail/{record_id}", response_model=record_schema.Record)
def record_detail_list(db: Session = Depends(get_db),
                  record_id=1):
    _user_list = detail_crud.get_detail_list(db,record_id=record_id)
    print("##") 
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return _user_list
    



@router.post("/detail-trytime-update")
def detail_trytime_update(db: Session = Depends(get_db)):
    _user_list = detail_crud.detail_trytime_update(db)
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return _user_list
    


