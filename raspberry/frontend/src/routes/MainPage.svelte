<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { school_class,is_login, access_token, username, school_number,school_id,school_name  } from "../lib/store"
    import {MAIN_CATEGORY} from "../lib/category"
    import moment from 'moment/min/moment-with-locales'
    
    let search_text = ""

    console.log($is_login)

    function func(e){
      if(e.keyCode==13){
        window.location.href = '/#/search/'+search_text;
		  }
    }
    /* 
    $: 는 svelte 에서 반응형 을 의미함, 즉 api 호출이 있으면 바뀐 total과 size에 대해 total_page를 구한다
    */
    /* $가 변수 앞에 변수 앞에 붙는 이유는 다른 변수들과의 이름이 중복되지 않도록, 잘쓰지 않는 기호를 앞에 붙여준거*/

    /* 로그인 시 사용할 함수들 */
    let page_school_number = $school_number
    let records = {}
    let error = {detail:[]}
    let rank = {}
    let UserName=$username
    let slice_cnt=3
    let Main_category = []
    for(const category_name of MAIN_CATEGORY){
        Main_category.push({category_name:category_name,cnt:0})
    }

    
    let gameplay_sum=0


    function get_record_all() { /*user의 record*/
        for(const [index, sub_category] of Main_category.entries()){
            records[sub_category.category_name]={record_list:[]}

            fastapi("get", "/api/record/record-by-category-all/" + page_school_number+"/"+sub_category.category_name, {}, (json) => {
                records[sub_category.category_name]=json
                Main_category[index].cnt=json.record_list.length
                records[sub_category.category_name].record_list = records[sub_category.category_name].record_list.slice(0,slice_cnt)
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
          <div class="card card-body">
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
        </div>
        <div>
          <div class="col-md-20">
            <div class="GAME-RECORD">
              <h5><b>최근 기록</b></h5>
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
                              {#each Array(4) as _, idx}
                                  <tr>
                                      <td>{100}점</td>
                                      <td>
                                          {#if (1)==0}
                                              {"0%"}
                                          {:else}
                                              {"100%"}
                                          {/if}
                                      </td>
                                      <td>
                                          {"YYYY년 MM월 DD일 a hh:mm"}
                                      </td>
                                      <td>
                                          <a use:link href="/profile/{page_school_number}/log/{123}">자세히 보기</a>
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
          <img src="../image/gameplay.png" alt="" class="mainpage_image" width="500">
          <div class="out-border">
            <a use:link href="/user-login" class="login_button">로그인</a>
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
  