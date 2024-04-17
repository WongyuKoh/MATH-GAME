
from pydantic import BaseModel,validator


class Problem(BaseModel):
    problem_in_number : str = ""
    category_number : int = 0
    
    class Config:
        from_attributes = True
        
class ProblemCreate(BaseModel):
    problem_in_number : str = ""
    category_number : int = 0

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
    
