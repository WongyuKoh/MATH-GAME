import datetime
from typing import Optional, Union

from pydantic import BaseModel,validator
from domain.detail.detail_schema import Detail


class Score(BaseModel):
    user_id : int = 0
    gametype : str = ""
    score : int = 0
    school_id : int = 0
    username : str = ""
    school_number : int = 0

    class Config:
        from_attributes = True
        
class ScoreCreate(BaseModel):
    user_id : int = 0
    gametype : str = ""
    score : int = 0

class Scorelist(BaseModel):
    scorelist : list[Score] = []