
from pydantic import BaseModel,validator


class School(BaseModel):
    school_name : str = ""
    school_id : int = 0
    address : str = ""
    
    class Config:
        from_attributes = True
        
class SchoolCreate(BaseModel):
    school_name : str = ""
    address : str = ""


class SchoolList(BaseModel):
    school_list : list[School] = []
    
class SchoolSearchList(BaseModel):
    serach_data_cnt : int = 0
    school_search_list : list[School] = []