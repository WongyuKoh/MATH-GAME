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
    import { is_login,school_number } from "../lib/store"
    import {MAIN_CATEGORY} from "../lib/category"
    import moment from 'moment/min/moment-with-locales'
    import { slide } from "svelte/transition";
    moment.locale('ko')

    export let params = {}
    let page_school_number = params.school_number
    let records = {}
    let error = {detail:[]}
    let username = ""
    let rank = {}
    let slice_cnt=3
    let Main_category = []
    for(const category_name of MAIN_CATEGORY){
        Main_category.push({category_name:category_name,cnt:0})
    }

    
    let gameplay_sum=0


    function get_record_all() { /*user의 record*/
        fastapi("get", "/api/user/username/" + page_school_number, {}, (json) => {
            username=json.username
        })
        for(const [index, sub_category] of Main_category.entries()){
            records[sub_category.category_name]={record_list:[]}

            fastapi("get", "/api/record/record-by-category-all/" + page_school_number+"/"+sub_category.category_name, {}, (json) => {
                records[sub_category.category_name]=json
                records[sub_category.category_name].record_list = records[sub_category.category_name].record_list.slice(0,slice_cnt)
                Main_category[index].cnt=json.record_list.length
                gameplay_sum+=Main_category[index].cnt
                if(Main_category[index].cnt==0){
                    rank[sub_category.category_name]="999+"

                }else{
                    fastapi("get", "/api/rank/user-profile/" + page_school_number + "/" + sub_category.category_name, {}, (json) => {
                        rank[sub_category.category_name] = json.rank
                    })
                }
            })
        }
    }

    function get_score() {
        fastapi("get", "/api/user/username/" + page_school_number, {}, (json) => {
            username=json.username
        })
        console.log("MAIN_category")
        console.log(Main_category)
        for(const [index, sub_category] of Main_category.entries()){
            console.log(Main_category[index].cnt,sub_category)
            console.log(sub_category.cnt,records,records[sub_category.category_name],records[sub_category.category_name].record_list.length)
            if(sub_category.cnt==0){
                rank[sub_category.category_name]="999+"

            }else{
                fastapi("get", "/api/rank/user-profile/" + page_school_number, {}, (json) => {
                    rank[sub_category.category_name] = json.rank
                })
            }
        }
    }


    get_record_all()


</script>

<div class="container">
    <div class="main-body">
        
        <div class="row gutters-sm">
            <div class="col-md-3 mb-3"><!-- md : 가로 사이즈, mb : 세로 사이즈-->
                <div class="card card-body">
                    <div class="d-flex flex-column align-items-center text-center">
                        <img src="https://i.ibb.co/CwwJsL4/init-profile.png" alt="Admin" class="rounded-circle" width="150">
                        <div class="mt-3">
                            <h4>{username}({page_school_number})</h4>
                            {#each MAIN_CATEGORY as category_name,i}
                                <p class="text-secondary mb-1">{category_name} : {rank[category_name]}등</p>
                            {/each}
                        </div>
                    </div>
                </div>
                <!-- 프로필 수정 버튼-->
                {#if page_school_number==$school_number}
                    <div class="align-items-right d-grid gap-2 d-md-flex justify-content-md-end">
                        <a use:link href="/profile/{page_school_number}/setting" class="btn btn-secondary btn-lg">
                            ⚙️
                        </a>
                    </div>
                {/if}
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
                                                    <a use:link href="/profile/{page_school_number}/log/{record.id}">자세히 보기</a>
                                                </td>
                                        {/each}
                                    </tbody>
                                </table>
                                <div class="text-center">
                                    <a use:link href="/profile/{page_school_number}/Record-Detail/{category_name}" class="btn btn-primary">더보기</a>
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