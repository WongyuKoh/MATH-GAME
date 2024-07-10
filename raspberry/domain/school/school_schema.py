
from pydantic import BaseModel,validator


class School(BaseModel):
    school_name : str = ""
    school_id : int = 0
    
    class Config:
        from_attributes = True
        
class SchoolCreate(BaseModel):
    school_name : str = ""


class SchoolList(BaseModel):
    problem_list : list[School] = []
    
