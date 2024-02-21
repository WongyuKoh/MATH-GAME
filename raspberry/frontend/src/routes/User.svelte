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
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    export let params = {}
    let school_number = params.school_number
    let records = {record_list:[]}
    let error = {detail:[]}
    let username = ""
    let rank = 0

    function get_record(category) { /*user의 record*/
        fastapi("get", "/api/record/record-by-category/" + school_number+"/"+category+"/10", {}, (json) => {
            records = json
        })
    }

    function get_score() {
        fastapi("get", "/api/rank/user-profile/" + school_number, {}, (json) => {
            rank = json.rank
            username = json.info.user_name
        })
    }


    get_record("test")
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

            <div class="col-md-7"> <!-- md : 가로 사이즈, mb : 세로 사이즈-->
                <h5><b>수열 기록</b></h5>
                <div class="card mb-3">
                    <div class="card-body">
                        <div class="row text-bg-dark p-3">
                            <div class="col-sm-3">
                                <h6 class="mb-0">점수</h6>
                            </div>
                            <div class="col-sm-3">
                                <h6 class="mb-0">정확도</h6>
                            </div>
                            <div class="col-sm-3">
                                <h6 class="mb-0">플레이 날짜</h6>
                            </div>
                            <div class="col-sm-3">
                                <h6 class="mb-0">자세히 보기</h6>
                            </div>
                        </div>
                        <hr>
                        {#each records.record_list as record, i}
                            <div class="row">
                                <div class="col-sm-3">
                                    <h6 class="mb-0">{record.score}점</h6>
                                </div>
                                <div class="col-sm-3">
                                    {#if (record.correct_pb_cnt+record.wrong_pb_cnt)==0}
                                    <h6 class="mb-0">0%</h6>
                                    {:else}
                                        <h6 class="mb-0">{Math.round(100*(record.correct_pb_cnt)/(record.correct_pb_cnt+record.wrong_pb_cnt))}%</h6>
                                    {/if}
                                </div>
                                <div class="col-sm-3"><!--moment(user.create_date).format("YYYY년 MM월 DD일 hh:mm a")-->
                                    <h6 class="mb-0">{moment(record.create_date).format("YYYY년 MM월 DD일")}</h6>
                                </div>
                                <div class="col-sm-3">
                                    <h6 class="mb-0">
                                        <a use:link href="/profile/{school_number}/log/{record.id}/">자세히 보기</a>
                                    </h6>
                                </div>
                            </div>
                            <hr>
                        {/each}
                    </div>
                </div>
                <div class="row gutters-sm">
                    <div class="col-sm-6 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <h6 class="d-flex align-items-center mb-3"><i class="material-icons text-info mr-2">assignment</i>Project Status</h6>
                                <small>Web Design</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 80%" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                                <small>Website Markup</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 72%" aria-valuenow="72" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                                <small>One Page</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 89%" aria-valuenow="89" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                                <small>Mobile Template</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 55%" aria-valuenow="55" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                                <small>Backend API</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 66%" aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                            </div>
                        </div>
                    </div>









                    
                    <div class="col-sm-6 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <h6 class="d-flex align-items-center mb-3"><i class="material-icons text-info mr-2">assignment</i>Project Status</h6>
                                <small>Web Design</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 80%" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                                <small>Website Markup</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 72%" aria-valuenow="72" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                                <small>One Page</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 89%" aria-valuenow="89" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                                <small>Mobile Template</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 55%" aria-valuenow="55" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                                <small>Backend API</small>
                                <div class="progress mb-3" style="height: 5px">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: 66%" aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>