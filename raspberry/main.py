# 192.168.0.2
# uvicorn main:app --reload
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.record import record_router
from domain.user import user_router
from domain.detail import detail_router
from domain.rank import rank_router
from domain.data_extract import de_router
from domain.problem_data import pbd_router
from domain.school import school_router

import uvicorn

app = FastAPI()

origins = [
    "http://localhost:8000"    # 또는 "http://localhost:5173"
]



app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(detail_router.router)
app.include_router(rank_router.router)
app.include_router(user_router.router)
app.include_router(record_router.router)
app.include_router(de_router.router)
app.include_router(pbd_router.router)
app.include_router(school_router.router)

if __name__ == "__main__":
    uvicorn.run(app)
    #uvicorn.run(app, host="0.0.0.0")# -> 배포시