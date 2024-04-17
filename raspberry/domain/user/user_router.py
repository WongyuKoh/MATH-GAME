from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from argon2.exceptions import VerificationError


from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

# https://velog.io/@munang/Python-FastAPI-%EC%9D%98%EC%A1%B4%EC%84%B1-%EC%A3%BC%EC%9E%85-Depends-%ED%95%A8%EC%88%98
# Depends 함수는 그 안에 있는 값을 먼저 실행함


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "23e8d781d997f31840bb859eb644c918181a6135b311ea0787deb58cf5f96b77"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)


@router.get("/list", response_model=user_schema.UserList)
def user_list(db: Session = Depends(get_db),
                  school_class : int = 1):
    total, _user_list = user_crud.get_user_list(
        db, school_class=school_class)
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return {
        'total': total,
        'user_list': _user_list
    }
    
# user 의 세부 정보를 알려주는 창
@router.get("/detail/{school_number}", response_model=user_schema.User)
def user_detail(school_number: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, school_number=school_number)
    return user

# 학번 입력시 유저 이름 알려주기
@router.get("/username/{school_number}", response_model=user_schema.UserName)
def user_detail(school_number: int, db: Session = Depends(get_db)):
    user = user_crud.get_username(db, school_number=school_number)
    return {"school_number":user.school_number,"username":user.username}

# --------------------------------
# 존재하는 학번인지 확인
@router.get("/user-exist/{school_number}", response_model=user_schema.UserExit)
def User_Exit(school_number: int, db: Session = Depends(get_db)):
    user_exit = user_crud.get_user_exit(db, school_number=school_number)
    return {"user_exit":user_exit} 


# 계정 삭제
@router.delete("/school-number-delete/{school_number}", status_code=status.HTTP_204_NO_CONTENT)
def User_delete(school_number: int, db: Session = Depends(get_db)):
    user_crud.user_delete(db, school_number=school_number)


# 비밀번호 변경
@router.post("/password-change/{school_number}", status_code=status.HTTP_204_NO_CONTENT)
def user_change_password(school_number: int, new_password: str, db: Session = Depends(get_db)):
    user_crud.user_password_change(db, school_number=school_number,new_password=new_password)

# 이름 변경 (아직)
@router.post("/username-change/{school_number}", status_code=status.HTTP_204_NO_CONTENT)
def user_change_username(school_number: int, new_username: str, db: Session = Depends(get_db)):
    user_crud.user_username_change(db, school_number=school_number,new_username=new_username)

# 학번 변경 (아직)
@router.post("/school-number-change/{school_number}", status_code=status.HTTP_204_NO_CONTENT)
def user_change_school_number(school_number: int, new_school_number: str, db: Session = Depends(get_db)):
    val=user_crud.user_school_number_change(db, school_number=school_number,new_school_number=new_school_number)
    if not val:
        raise HTTPException(status_code=404, detail="user not found")

# -----------------------------------


# user 생성
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    print(user)
    if user: # 409 Conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    

    
    user_crud.create_user(db=db, user_create=_user_create)
    
@router.post("/score-updatebyinput", status_code=status.HTTP_204_NO_CONTENT)
def user_list(db: Session = Depends(get_db),
                  category : str = "", school_number : int = 0, score : int = 0):
    
    user_crud.user_score_updatebyinput(
        db, school_number=school_number,category=category,score = score)
    
@router.post("/score-updatebyrecord", status_code=status.HTTP_204_NO_CONTENT)
def user_list(db: Session = Depends(get_db),
                   school_number : int = 0):
    
    user_crud.user_score_updatebyrecord(
        db, school_number=school_number)
    
@router.post("/score-update-all", status_code=status.HTTP_204_NO_CONTENT)
def user_list(db: Session = Depends(get_db)):
    
    user_crud.user_score_update_all(db)
    
@router.get("/score", response_model=user_schema.UserScore)
def user_score(db: Session = Depends(get_db),
                  category : str = "", school_number : int = 0):
    
    score = user_crud.user_score(
        db, school_number=school_number,category=category)
    
    return {"score":score}
    
        


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    #print(f"form_data.username : {form_data.username}")
    user = user_crud.get_user2name(db, form_data.username)
    # user.password : hash 값, form_data.password : 입력값
    try:
        if not user or not pwd_context.verify(user.password,form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="아이디 또는 비밀번호가 잘못되었습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except VerificationError:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="아이디 또는 비밀번호가 잘못되었습니다.",
                headers={"WWW-Authenticate": "Bearer"},
                )    

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "school_number": str(user.school_number)
    }
    
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        #print(f'get_current_user user name : {username}')
        user = user_crud.get_user2name(db, username=username)
        if user is None:
            raise credentials_exception
        return user
    
