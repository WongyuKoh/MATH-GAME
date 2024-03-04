from pydantic import BaseModel, validator, EmailStr
from domain.record.record_schema import Record


# api 입 

class UserCreate(BaseModel):
    school_number: int # 학번
    username : str # 실명
    password1: str
    password2: str

    @validator('username', 'password1', 'password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    

    @validator('password2')
    def passwords_match(cls, v, values):
        # passwords_match 메서드의 info 매개변수의 info.data에는 UserCreate의 속성들이 {변수명:값, ...} 형태로 전달된다.
        # info.data = values
        if 'password1' in values and v != values['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
    
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str # 학번
    school_number : str
    
class User(BaseModel):
    school_number : int
    username: str
    records : list[Record] =[]
    
    class Config:
        from_attributes = True
        
class UserName(BaseModel):
    school_number : int
    username: str
    
    class Config:
        from_attributes = True
        
class UserList(BaseModel):
    total: int = 0
    user_list : list[User] = []
    
class UserExit(BaseModel):
    user_exit : bool = True
    
