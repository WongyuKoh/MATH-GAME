
from pydantic import BaseModel,validator


class Problem(BaseModel):
    id : int = 0
    problem : str = ""
    problem_list : str = "" 
    category : str = ""
    trytime : int = 0
    trystudent : int = 0
    problem_level : int = 0
    bundles_idx_list : str = "" # 음수 값 들어가는 건 그 값을 idx 가 아닌 실제로 이용하겠다는 의미, - 를 붙여서 사용
    answer : int = 0
    
    class Config:
        from_attributes = True
        
class ProblemCreate(BaseModel):
    problem : str = ""
    category : str = ""
    bundles_idx_list : str = "" # 음수 값 들어가는 건 그 값을 idx 가 아닌 실제로 이용하겠다는 의미, - 를 붙여서 사용\
    trytime : int = 0
    answer : int  = 0


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
    
class Problem_Emit(BaseModel):
    problem : str = ""
    category : str = ""
    answer : int  = 0
    problem_level : int = 0
    
class Problem_emit_list(BaseModel):
    cnt : int = 0
    problem_list : list[Problem_Emit] = []