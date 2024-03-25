from pydantic import BaseModel, validator, EmailStr
from domain.record.record_schema import Record
import datetime

# api 입력


class Detaildb(BaseModel):
    id : int
    category : str
    problem : str
    problem_answer : str
    user_answers : str
    record_id : int

class Recorddb(BaseModel):
    id : int
    score : int
    correct_pb_cnt : int
    wrong_pb_cnt : int
    create_date : datetime.datetime
    user_name : str
    user_id : int
    
    
class Userdb(BaseModel):
    school_number : int
    username : str
    password : str
    
class DetaildbList(BaseModel):
    dblist : list[Detaildb] = []

class RecorddbList(BaseModel):
    dblist : list[Recorddb] = []
    
    
class UserdbList(BaseModel):
    dblist : list[Userdb] = []
    
