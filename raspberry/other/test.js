const fastapi = (url, params, success_callback, failure_callback) => {
    let method = "post"
    let content_type = 'application/json'
    let body = JSON.stringify(params) /*{"content":"입력"}*/

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }
    /*요거는 지웠어요 흠 이거 코드가 더 전 코드인거같네요 딴거 찾아볼께요 */
    /*
    const _access_token = get(access_token)
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
    }
    */

    if (method !== 'get') {
        options['body'] = body
    }

    fetch(_url, options)
        .then(response => { /* fetch 를 통해 들어온 값이 then 의 response 에 입력되서 then 안에 있는 임의 함수를 실행함*/
            
        if(response.status === 204) {  // No content
                if(success_callback) {
                    success_callback()
                }
                return
            }
            response.json()
                .then(json => {


                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) {                 

                            success_callback(json)
                        
                        }
                        return

                    }else {
                        if (failure_callback) {
                            failure_callback(json)
                        }else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    alert(JSON.stringify(error))
                })
        })
}

let params = {
    main_category:"지수",
    correct_pb_cnt: 1,
    wrong_pb_cnt : 2,
    score : 3,
    detail:[
        {
            category:"111",
            problem:"asdasd",
            problem_answer:"123",
            user_answers:"fffff"
        }
    ]


}

fastapi( "http://127.0.0.1:8000/api/record/create/20402/", params, (json) => {
    records = json
})

/**
 upload={
    "main_category": "수열",
    "correct_pb_cnt": 4440,
    "wrong_pb_cnt": 3330,
    "score": 144231330,
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

 */