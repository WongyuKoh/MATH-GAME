from pydantic import BaseModel, validator, EmailStr
from domain.record.record_schema import Record,nodetail_Record
import datetime


class StudentEvaluate(BaseModel):
    score : int
    level : int
    
        