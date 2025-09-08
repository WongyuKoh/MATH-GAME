from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.problem_data import pbd_schema,pbd_crud
router = APIRouter(
    prefix="/api/problem",
)
# ----- problem ------ 

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def problem_create(_problem_create: pbd_schema.ProblemCreate,
                  db: Session = Depends(get_db)):
    
    
    
    pbd_crud.create_problem(db=db,problem_create=_problem_create,
                            trytime=_problem_create.trytime,main_category=_problem_create.main_category)


@router.post("/problem-update", status_code=status.HTTP_204_NO_CONTENT)
def problem_create(db: Session = Depends(get_db)):
    

    pbd_crud.problem_update(db=db)

# problem_list 업데이트도 만들기

@router.post("/problem-trytime-update", status_code=status.HTTP_204_NO_CONTENT)
def problem_create(db: Session = Depends(get_db)):
    
    pbd_crud.problem_trytime_update(db=db)
    

@router.post("/bundles-idx-list-update", status_code=status.HTTP_204_NO_CONTENT)
def bundles_create(db: Session = Depends(get_db)):
    
    pbd_crud.bundles_update(db=db)


@router.post("/problem-answer-update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(db: Session = Depends(get_db)):
    
    pbd_crud.answer_update(db=db)


@router.get("/problem-emit",response_model=pbd_schema.Problem_emit_list)
def problem_emit(db:Session = Depends(get_db),
                 school_number : int = 0, school_name : str = "",cnt : int = 0,category : str = ""):
    
    result = pbd_crud.problem_emit(db=db,school_number=school_number,school_name=school_name,cnt = cnt,category=category)
    
    return result