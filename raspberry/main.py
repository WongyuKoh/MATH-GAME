# 192.168.0.2
# uvicorn main:app --reload
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.record import record_router
from domain.user import user_router
from domain.detail import detail_router
from domain.rank import rank_router

app = FastAPI()

origins = [
    "http://localhost:5173",    # 또는 "http://localhost:5173"
]

#fjfjf

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(detail_router.router)
app.include_router(rank_router.router)
app.include_router(user_router.router)
app.include_router(record_router.router)