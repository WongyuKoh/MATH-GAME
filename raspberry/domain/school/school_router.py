from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.school import school_schema,school_crud
router = APIRouter(
    prefix="/api/school",
)
# ----- problem ------ 

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def school_create(_school_create: school_schema.SchoolCreate,
                  db: Session = Depends(get_db)):
    
    
    
    school_crud.create_school(db,_school_create.school_name)

@router.get("/list",response_model=school_schema.SchoolList)
def school_list(db:Session = Depends(get_db)):
    
    return school_crud.school_list(db)