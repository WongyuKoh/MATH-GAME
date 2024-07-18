import datetime
from typing import Optional, Union

from pydantic import BaseModel,validator
from domain.detail.detail_schema import Detail


class Gametype(BaseModel):
    typename : str = ""
    school_id : int = 0
    id : int = 0

    class Config:
        from_attributes = True
        
class GametypeCreate(BaseModel):
    school_name : str = ""
    typename : str = ""

class GametypeList(BaseModel):
    gametype_list : list[Gametype] = []