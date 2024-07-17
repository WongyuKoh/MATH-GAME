<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import {is_login, access_token, username, school_number,school_id,school_name,rank_category_page  } from "../lib/store"
    import {MAIN_CATEGORY} from "../lib/category"
    import moment from 'moment/min/moment-with-locales'
    
    const emojis = {
        "1st" : "🥇",
        "2nd" : "🥈",
        "3rd"  : "🥉",
        "no_medal" : ""
    }


    let search_text = ""

    function func(e){
      if(e.keyCode==13){
        if(search_text==""){
            window.location.href = '/#/search/noinput';
        }else{
            window.location.href = '/#/search/'+search_text;
        }
		  }
    }
    /* 
    $: 는 svelte 에서 반응형 을 의미함, 즉 api 호출이 있으면 바뀐 total과 size에 대해 total_page를 구한다
    */
    /* $가 변수 앞에 변수 앞에 붙는 이유는 다른 변수들과의 이름이 중복되지 않도록, 잘쓰지 않는 기호를 앞에 붙여준거*/

    /* 로그인 시 사용할 함수들 */
    let page_school_number = $school_number
    let error = {detail:[]}
    let rank = {}
    let UserName=$username
    let slice_cnt=4
    let records=[]
    let Main_category = []
    let user_list = []
    let user_class = Math.floor(page_school_number/100)%10
    const total_page = 9
    for(const category_name of MAIN_CATEGORY){
        Main_category.push({category_name:category_name,cnt:0})
    }

    function get_user_list(_school_class) {
        let params={
          school_class : _school_class
        }
        fastapi('get', '/api/record/record-class-cnt-all', params, (json) => {
            user_list = json.record_class
            console.log('----')
            console.log(user_list)

        })

    }
    
    let gameplay_sum=0

    function get_record_recent(){
      fastapi("get", "/api/user/detail/" + page_school_number, {}, (json) => {
        records=json.records
        records = records.slice(records.length-slice_cnt,records.length).reverse()

      })

    }


    function get_record_all() { /*user의 record*/
        for(const [index, sub_category] of Main_category.entries()){

            fastapi("get", "/api/record/record-by-category-all/" + page_school_number+"/"+sub_category.category_name, {}, (json) => {
                Main_category[index].cnt=json.record_list.length
                gameplay_sum+=Main_category[index].cnt
                if(Main_category[index].cnt==0){
                    rank[sub_category.category_name]="999+"

                }else{
                    User_Rank(page_school_number,sub_category.category_name)

                }
            })
        }
    }
    function User_Rank(school_number,category) {

        let value=0
        fastapi("get", "/api/rank/user-profile/" + school_number + "/" + category, {}, (json) => {
            value=json.rank
            //console.log(value,json)
            if(value==0 || value==-1){
                rank[category] = "999+"
            }else{
                rank[category] = value
            }
            //console.log('!!',rank[category],category)
        })
    }
    if($is_login){
      get_record_all()
      get_record_recent()
      get_user_list(user_class)
    }


  </script>

<!--
  https://aboooks.tistory.com/59
  tr  : table row, 가로줄 만드는거(데이터 들어가는 라인의 가장 윗부분 대로)
  th : table head , 표의 제목
  td : table data, 셀을 만드는 역할
-->

<div class="container my-3">
  {#if $is_login }
    <div class="SCREEN_login">
      <div class="mainscreen_login">
        <div class="user_profile">
          <a href="#/profile/{page_school_number}/" style="text-decoration:none; color:black">
            <div class="card card-body active-profile">
              <div class="d-flex flex-column align-items-center text-center">
                  <img src="https://i.ibb.co/CwwJsL4/init-profile.png" alt="Admin" class="rounded-circle user_image" width="150">
                  <div class="mt-3">
                      <h4>{UserName}({page_school_number})</h4>
                      {#each MAIN_CATEGORY as category_name,i}
                          <p class="text-secondary mb-1">{category_name} : {rank[category_name]}등</p>
                      {/each}
                  </div>
              </div>
            </div>
          </a>
        </div>
        <div class="recent-record">
          <div class="col-md-20">
            <div class="GAME-RECORD">
              <h5><b><i>최근 기록(Recent Record)</i></b></h5>
              <div class="card mb-3">
                  <div class="card-body">
                      <table class="table text-center"> <!-- 부트스 트랩 5 버전의 이름만 가지고 와서 사용하면 됨-->
                          <thead class="table-dark">
                          <tr>
                              <th scope="col">게임 유형</th>
                              <th scope="col">점수</th>
                              <th scope="col">정확도</th>
                              <th scope="col">플레이 날짜</th>
                              <th scope="col">detail</th>
                          </tr>
                          </thead>
                          <tbody>
                              {#each records as recent_record, idx}
                                  <tr>
                                      <td>{recent_record.main_category}</td>
                                      <td>{recent_record.score}점</td>
                                      <td>
                                          {#if (recent_record.trytime)==0}
                                            {"0%"}
                                          {:else}
                                            {Math.round(100*(recent_record.correct_pb_cnt)/(recent_record.trytime))}%
                                          {/if}
                                      </td>
                                      <td>
                                        {moment(recent_record.create_date).format("YYYY년 MM월 DD일 a hh:mm")}
                                      </td>
                                      <td>
                                          <a use:link href="/profile/{page_school_number}/log/{recent_record.id}">자세히 보기</a>
                                      </td>
                              {/each}
                          </tbody>
                      </table>
                      <div class="text-center">
                          <a use:link href="/profile/{page_school_number}/Record-Detail/{43}" class="btn btn-primary">더보기</a>
                      </div>
                  </div>
              </div>
            </div>
          </div>
        </div>
        <div class="class_info_rank">
          <div class="game_start_button">
            <a use:link href="/game" class="login_game_start_button">게임 시작</a>
            <a use:link href="/game" class="login_game_start_button">게임 방법</a>
  
          </div>
          <div class="class_info">
            <div class="card mb-3">
              <div class="card-body">
                <table class="table">
                  <thead>
                    <tr class="text-center table-dark">
                        <th>번호</th>
                        <th>이름</th>
                        <th>플레이 횟수</th>
                    </tr>
                    </thead>
                    <tbody>
                      {#each user_list as user, i}
                        {#if i<10}
                          <tr class="text-center">
                              <td>{user.school_number}</td> 
                              <td>
                                  <a use:link href="/profile/{Number(user.school_number)}">{user.username}</a>
                              </td>
                              <td>{user.record_cnt}</td>
                              <!--<td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>-->
                          </tr>
                        {/if}
                      {/each}
                    </tbody>
                </table>
                <div class="text-center">
                    <a use:link href="/home/{user_class}" class="btn btn-primary">더보기</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  {:else}
    <div class="SCREEN">

      <div class="mainscreen">
        <div class="search-display">
          <a use:link href="/search/{search_text}"> <!-- 잘 작동함-->
            <img src="../image/search_blue.svg" alt="" class="search-button" width="45">
          </a>
          
          <input type="text" class="school-search" id="username" bind:value="{search_text}" on:keydown={func} placeholder="학교명을 검색하세요.">
          
          
        
        </div>
        <div class="unlogin-screen">
          <img src="../image/start_ui_3.png" alt="" class="mainpage_image" width="500">
          <div class="out-border">
            <a use:link href="/user-login/none" class="login_button">로그인</a>
            <a use:link href="/user-create" class="school_button">회원가입</a>
            <a use:link href="/game" class="school_button">학교등록</a>
            <a use:link href="/game" class="login_button">게임</a>
          </div>
          
        </div>
        <!--<div>
          세로로
          <div class="unlogin-button">
            <a href="#" class="BUTTON_XAB">Login</a>
            
            <a href="#" class="BUTTON_XAB">Login</a>
            학교 등록, 로그인 가로로 나타내기

          </div>-->
        <div>
          <!--게임하러 가기 버튼-->

        </div>
        <div>
          <!-- 게임 플레이 이미지 또는 영상 -->
        </div>



      </div>

    </div>
  {/if}
</div>
  