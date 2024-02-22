<!--
{
  "school_number": 20402,
  "username": "고원규",
  "records": [
    {
      "id": 1,
      "correct_pb_cnt": 123,
      "wrong_pb_cnt": 333,
      "score": 5422,
      "create_date": "2024-02-18T16:14:12.862612",
      "detail": []
    },
    {
      "id": 2,
      "correct_pb_cnt": 4,
      "wrong_pb_cnt": 2,
      "score": 444123,
      "create_date": "2024-02-18T17:10:42.132324",
      "detail": []
    },
    {
      "id": 3,
      "correct_pb_cnt": 444,
      "wrong_pb_cnt": 23,
      "score": 55,
      "create_date": "2024-02-18T17:46:14.005700",
      "detail": [
        {
          "category": "a",
          "problem": "b",
          "problem_answer": "c",
          "user_answers": "d"
        }
      ]
    }
  ]





-->

<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push,link } from 'svelte-spa-router'
    import { is_login } from "../lib/store"
    import {MAIN_CATEGORY} from "../lib/category"
    import moment from 'moment/min/moment-with-locales'
    import { slide } from "svelte/transition";
    moment.locale('ko')

    export let params = {}
    let school_number = params.school_number
    let records = {}
    let error = {detail:[]}
    let username = ""
    let rank = 0
    let slice_cnt=3
    let Main_category = []
    for(const category_name of MAIN_CATEGORY){
        Main_category.push({category_name:category_name,cnt:0})
    }

    
    let gameplay_sum=0

    function get_record(category) { /*user의 record*/
        fastapi("get", "/api/record/record-by-category/" + school_number+"/"+category+"/3", {}, (json) => {
            records = json
        })
    }

    function get_record_all() { /*user의 record*/
        for(const [index, sub_catgeory] of Main_category.entries()){
            records[sub_catgeory.category_name]={record_list:[]}

            fastapi("get", "/api/record/record-by-category-all/" + school_number+"/"+sub_catgeory.category_name, {}, (json) => {
                records[sub_catgeory.category_name]=json
                records[sub_catgeory.category_name].record_list = records[sub_catgeory.category_name].record_list.slice(0,slice_cnt)
                Main_category[index].cnt=json.record_list.length
                gameplay_sum+=Main_category[index].cnt
            })
        }
    }

    function get_score() {
        fastapi("get", "/api/rank/user-profile/" + school_number, {}, (json) => {
            rank = json.rank
            username = json.info.user_name
        })
    }


    get_record_all()
    get_score()

</script>

<link href="raspberry_database/frontend/src/app.css" rel="stylesheet" type="text/css" />

<div class="container">
    <div class="main-body">
        
        <div class="row gutters-sm">
            <div class="col-md-3 mb-3"><!-- md : 가로 사이즈, mb : 세로 사이즈-->
                <div class="card card-body">
                    <div class="d-flex flex-column align-items-center text-center">
                        <img src="https://i.ibb.co/CwwJsL4/init-profile.png" alt="Admin" class="rounded-circle" width="150">
                        <div class="mt-3">
                            <h4>{username}({school_number})</h4>
                            <p class="text-secondary mb-1">{rank}등</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 밑에 내용 -->
            

            <!-- 게임 기록 --><!-- md : 가로 사이즈, mb : 세로 사이즈-->
            <div class="col-md-7">
                <div class="GAME-RECORD">
                    {#each MAIN_CATEGORY as category_name, i}
                        <h5><b>{category_name}</b></h5>
                        <div class="card mb-3">
                            <div class="card-body">
                                <table class="table text-center"> <!-- 부트스 트랩 5 버전의 이름만 가지고 와서 사용하면 됨-->
                                    <thead class="table-dark">
                                    <tr>
                                        <th scope="col">점수</th>
                                        <th scope="col">정확도</th>
                                        <th scope="col">플레이 날짜</th>
                                        <th scope="col">detail</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                        {#each records[category_name].record_list as record, i}
                                            <tr>
                                                <td>{record.score}점</td>
                                                <td>
                                                    {#if (record.correct_pb_cnt+record.wrong_pb_cnt)==0}
                                                        {"0%"}
                                                    {:else}
                                                        {Math.round(100*(record.correct_pb_cnt)/(record.correct_pb_cnt+record.wrong_pb_cnt))}%
                                                    {/if}
                                                </td>
                                                <td>
                                                    {moment(record.create_date).format("YYYY년 MM월 DD일 hh:mm")}
                                                </td>
                                                <td>
                                                    <a use:link href="/profile/{school_number}/log/{record.id}">자세히 보기</a>
                                                </td>
                                        {/each}
                                    </tbody>
                                </table>
                                <div class="text-center">
                                    <a use:link href="/profile/{school_number}/Record-Detail/{category_name}" class="btn btn-primary">더보기</a>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
                <div class="row gutters-sm">
                    <div class="col-sm-6 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <h6 class="d-flex align-items-center mb-3"><b>게임 시도 횟수</b></h6>
                                {#each Main_category as sub_category, i}

                                
                                    <small>{sub_category.category_name}({sub_category.cnt} times)</small>
                                    <div class="progress mb-3" style="height: 5px">
                                        <div class="progress-bar bg-primary" role="progressbar" style="width: {(sub_category.cnt/gameplay_sum)*100}%" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</div>