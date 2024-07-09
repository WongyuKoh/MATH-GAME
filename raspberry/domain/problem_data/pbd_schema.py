
from pydantic import BaseModel,validator


class Problem(BaseModel):
    id : int = 0
    problem : str = ""
    problem_list : str = "" 
    category : str = ""
    trytime : int = 0
    trystudent : int = 0
    problem_level : int = 0
    
    
    class Config:
        from_attributes = True
        
class ProblemCreate(BaseModel):
    problem : str = ""
    category : str = ""


class ProblemList(BaseModel):
    problem_list : list[Problem] = []
    
    
class ProblemTitle(BaseModel):
    title : str = ""
    title_number : int = 0
    
    class Config:
        from_attributes = True
    
        
class ProblemTitleCreate(BaseModel):
    title : str = ""

class Problem_TitleList(BaseModel):
    problem_title_list : list[ProblemTitle] = []
    
