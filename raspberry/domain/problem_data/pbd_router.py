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
    
    
    
    pbd_crud.create_problem(db=db,problem_create=_problem_create)


@router.post("/problem-update", status_code=status.HTTP_204_NO_CONTENT)
def problem_create(db: Session = Depends(get_db)):
    

    pbd_crud.problem_update(db=db)



@router.post("/problem-trytime-update", status_code=status.HTTP_204_NO_CONTENT)
def problem_create(db: Session = Depends(get_db)):
    
    pbd_crud.problem_trytime_update(db=db)




        
        
# @router.get("/list/{category_number}", response_model=pbd_schema.ProblemList)
# def problem_list(db: Session = Depends(get_db),
#                   category_number : int = 0):

#     problem_list = pbd_crud.get_problem(
#         db, category_number=category_number)
    
#     return problem_list

# @router.get("/titlename2number/{title_name}", response_model=pbd_schema.ProblemTitle)
# def problem_list(db: Session = Depends(get_db),
#                   title_name : str = ""):

#     title_number = pbd_crud.Title_name2number(
#         db, title_name=title_name)
    
    
#     return {"title":title_name,"title_number":title_number}


# # ---- title -----

# @router.post("/title/create", status_code=status.HTTP_204_NO_CONTENT)
# def title_create(_title_create: pbd_schema.ProblemTitleCreate,
#                   db: Session = Depends(get_db)):
    
#     pbd_crud.create_title(db=db,problem_create=_title_create)

        
# @router.get("/title/list", response_model=pbd_schema.Problem_TitleList)
# def title_list(db: Session = Depends(get_db)):

#     title_list = pbd_crud.get_title(db)
    
#     return title_list