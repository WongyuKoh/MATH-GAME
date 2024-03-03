import requests
from datetime import datetime
upload={
    "main_category": "",
    "correct_pb_cnt": 4440,
    "wrong_pb_cnt": 3330,
    "score": 144231330,
    "user_name": "",
    "create_date": str(datetime.now()),
    "detail": [
        {
        "category": "1112222",
        "problem": "33334444",
        "problem_answer": "qqqqqwwww",
        "user_answers": "ddddzzzxss"
        }
    ]
}
        
requests.post("http://127.0.0.1:8000/api/record/create/20402/", json=upload)