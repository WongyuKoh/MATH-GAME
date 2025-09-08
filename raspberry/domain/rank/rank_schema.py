from pydantic import BaseModel, validator, EmailStr

class Rank(BaseModel):
    school_number : int = 11111
    username : str = ""
    score : int = 0
    school_id : int = 0
    

    
    class Config:
        from_attributes = True

class RankList(BaseModel):
    rank_list : list[Rank] = []
    
    
class Rank_User(BaseModel):
    rank : int = 0
    info : Rank = []
