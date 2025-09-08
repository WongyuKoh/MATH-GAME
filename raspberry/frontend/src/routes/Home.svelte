<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { school_class,is_login, access_token, school_number  } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    export let params = {}

    let user_list = []
    let income_class = params.class
    const total_page = 9
    let first_income = false
    /* 
    '/home/:class'
    $: 는 svelte 에서 반응형 을 의미함, 즉 api 호출이 있으면 바뀐 total과 size에 대해 total_page를 구한다
    */
    /* $가 변수 앞에 변수 앞에 붙는 이유는 다른 변수들과의 이름이 중복되지 않도록, 잘쓰지 않는 기호를 앞에 붙여준거*/
    

    let classcategorylist=[]
    function get_user_list(income_class,_school_class) {
        if(!first_income){
          _school_class = income_class
        }

        /* let params={
          school_class : _school_class
        }
        fastapi('get', '/api/record/record-class-cnt-all', params, (json) => {
            user_list = json.record_class
            $school_class = _school_class
            first_income = true

        }) */

        fastapi('get', '/api/record/category_try/'+_school_class, params, (json) => {
            classcategorylist = json.classcategorylist
            user_list.length=classcategorylist.length
            user_list.fill(0)
            first_income = true
            updatetext()

        })

    }
    
    let gameplay_sum=0

    let records = {}
    let error = {detail:[]}
    let Main_category = []

    let MAIN_CATEGORY = []
    let gametypelist = []
    let select_categorylist = []
    fastapi("get", "/api/gametype/type-list", {}, (json) => {
        gametypelist=json.gametype_list
        MAIN_CATEGORY = []
        for(const gametype of gametypelist){

            MAIN_CATEGORY.push(gametype.typename)
            Main_category.push({category_name:gametype.typename,cnt:0})
        }
        select_categorylist.length=MAIN_CATEGORY.length
        //console.log('!!!',select_categorylist.length)
        select_categorylist.fill(1)
        get_user_list(income_class)
        //get_record_all()
    })



    /*
    function get_question_list() {
      fetch("http://127.0.0.1:8000/api/question/list").then((response) => {
        response.json().then((json) => {
          question_list = json
        })
      })
      fastapi('get', '/api/question/list', {}, (json) => {
            question_list = json.question_list
        })
    }
  
    get_question_list()*/

    let trytimetext=""

    function trytimeupdate(i){
        select_categorylist[i]=(select_categorylist[i]+1)%2
        updatetext()

    }
    function updatetext(){
        trytimetext=""
        for(let k=0;k<user_list.length;k++){
            user_list[k]=0
        }
        for(let j=0;j<select_categorylist.length;j++){
            if(select_categorylist[j]){
                for(let k=0;k<user_list.length;k++){
                    //console.log(j,k,classcategorylist[k].category[Main_category[j].category_name])
                    user_list[k]+=classcategorylist[k].category[Main_category[j].category_name]

                }
                if(trytimetext!=""){
                    trytimetext+=", "
                }
                trytimetext+=MAIN_CATEGORY[j]
            }
        }
        trytimetext+=" 플레이 횟수"
    }

  </script>

<!--
  https://aboooks.tistory.com/59
  tr  : table row, 가로줄 만드는거(데이터 들어가는 라인의 가장 윗부분 대로)
  th : table head , 표의 제목
  td : table data, 셀을 만드는 역할
-->

<div class="container my-3">
    <!-- 카테고리 선택 -->
     
    <ul class="pagination justify-content-center">
        {#each MAIN_CATEGORY as sub_category,i}
            {#if select_categorylist.length>i}
                <li class="page-item {(select_categorylist[i]) && "active"}">
                    <button on:click="{() => trytimeupdate(i)}" class="page-link">{sub_category}</button>
                </li>
            {:else}
                <li class="page-item disabled">
                    <button class="page-link">{sub_category}</button>
                </li>
            {/if}
        {/each}
    </ul>
    


    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th style="width:33%">번호</th>
            <th style="width:34%">이름</th>
            <th style="width:33%">{trytimetext}</th>
        </tr>
        </thead>
        <tbody>
        {#each classcategorylist as user, i}
        <tr class="text-center">
            <td>{user.school_number}</td> 
            <td>
                <a use:link href="/profile/{Number(user.school_number)}">{user.username}</a>
            </td>
            <td>{user_list[i]}</td>
            <!--<td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>-->
        </tr>
        {/each}
        </tbody>
    </table>

    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$school_class <= 1 && 'disabled'}">
            <button class="page-link" on:click="{() => get_user_list(income_class,$school_class-1)}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page+1) as _, loop_page}
        {#if loop_page!=0} 
            <li class="page-item {loop_page === $school_class && 'active'}">
            <button on:click="{() => get_user_list(income_class,loop_page)}" class="page-link">{loop_page}</button>
            </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$school_class >= total_page && 'disabled'}">
            <button class="page-link" on:click="{() => get_user_list(income_class,$school_class+1)}">다음</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->

  
</div>
  