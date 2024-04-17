from models import PROBLEM,PROBLEM_TITLE
from sqlalchemy.orm import Session
import datetime
from domain.problem_data.pbd_schema import ProblemCreate,ProblemTitleCreate

def create_problem(db: Session,
                  problem_create: ProblemCreate):
    
    db_problem = PROBLEM(
        problem_in_number=problem_create.problem_in_number,
        category_number=problem_create.category_number
                         )
    db.add(db_problem)
    db.commit()
    
    return db_problem

def get_problem(db: Session, category_number : int = 0):
    _get_problem = db.query(PROBLEM).filter(PROBLEM.category_number==category_number).all()

    return _get_problem

def Title_name2number(db: Session, title_name : str = ""):
    get_title_number = db.query(PROBLEM_TITLE).filter(PROBLEM_TITLE.title==title_name).first().title_number

    return get_title_number



def create_title(db: Session,
                  problem_create: ProblemTitleCreate):
    

    number=int(db.query(PROBLEM_TITLE).count()+1)

    db_problem_title = PROBLEM_TITLE(
        title=problem_create.title,
        title_number=number)
    
    
    db.add(db_problem_title)
    db.commit()
    
    return db_problem_title


def get_title(db: Session):
    _get_title = db.query(PROBLEM_TITLE).all()
    return _get_title