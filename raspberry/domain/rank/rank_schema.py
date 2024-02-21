from pydantic import BaseModel, validator, EmailStr


class Rank(BaseModel):
    id : int = 0
    user_id : int = 11111
    user_name : str = ""
    score : int = 0
    
    
    class Config:
        from_attributes = True

class RankList(BaseModel):
    rank_list : list[Rank] = []
    
    
class Rank_User(BaseModel):
    rank : int = 0
    info : Rank = []
