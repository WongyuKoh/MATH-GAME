<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { is_login, access_token,search_school_page  } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('en')
    let search_text = ""

    export let params = {}

    let search_school_list = ""
    let site_search_text = params.search_text
    let search_data_cnt = 1
    let total_page = 1

  /*'/search/:search_text'*/

    function search_result(search_text,_search_school_page) { /* 1<=page<=total_page*/
        if(search_text=="noinput"){
            search_text=""
        }
        let params = {
            search_text : search_text,
            search_data_cnt : search_data_cnt,
            now_page : _search_school_page

        }
        fastapi("get", "/api/school/limited-search-list", params, (json) => {

            if(json.search_data_cnt==0){
                total_page = 1
            }else{
                total_page = (json.serach_data_cnt-1)/search_data_cnt + 1
            }
            search_school_list = json.school_search_list
            site_search_text = search_text
            $search_school_page = _search_school_page
            console.log(search_school_list)
            
        })
    }

    function func(e){
        if(e.keyCode==13){
            if(search_text==""){
                window.location.href = '/#/search/noinput';
                search_result('noinput',1)
            }else{
                window.location.href = '/#/search/'+search_text;
                search_result(search_text,1)
            }   
		}
    }
    /* 
    $: 는 svelte 에서 반응형 을 의미함, 즉 api 호출이 있으면 바뀐 total과 size에 대해 total_page를 구한다
    */
    /* $가 변수 앞에 변수 앞에 붙는 이유는 다른 변수들과의 이름이 중복되지 않도록, 잘쓰지 않는 기호를 앞에 붙여준거*/

    $:search_result(site_search_text,1)

</script>

<!--
https://aboooks.tistory.com/59
tr  : table row, 가로줄 만드는거(데이터 들어가는 라인의 가장 윗부분 대로)
th : table head , 표의 제목
td : table data, 셀을 만드는 역할
-->
<div class="container my-3">

  <div class="SCREEN">

    <div class="mainscreen">
        <div class="search-display">
        <a use:link href="/search/{search_text}">
            <img src="../image/search_blue.svg" alt="" class="search-button" width="45">
        </a>
        
        <input type="text" class="school-search" id="username" bind:value="{search_text}" on:keydown={func} placeholder="학교명을 검색하세요.">
        
        
        
        </div>


    </div>

  </div>
  <div class="row">

    <div class="col-sm-10 mr-0">
        <div class="card ccard radius-t-0 h-100">
            <div class="position-tl w-102 border-t-3 brc-primary-tp3 ml-n1px mt-n1px"></div>
            <div class="card-header pb-3 brc-secondary-l3">
                <h5 class="card-title mb-2 mb-md-0 text-dark-m3 text-center">
                    "{site_search_text}" 검색 목록
                </h5>
            </div>
            {#each search_school_list as _school_name, i}
                {#if i<search_data_cnt}
                  <div class="card-body pt-2 pb-1">
                      <a href="/#/user-login/{_school_name.school_name}" style="text-decoration:none; color:black">
                          <div role="button" class="d-flex flex-wrap align-items-center my-2 bgc-secondary-l4 bgc-h-secondary-l3 radius-1 p-25 d-style jc_sb">
                              
                              <div class="medal-rank-blank">
                                  <span class="mr-25 w-5 text-center">
                                      {($search_school_page-1)*search_data_cnt+i+1}
                                  </span>
                                  <span class="mr-25 w-4 h-4 overflow-hidden text-center border-1 brc-secondary-m2 radius-round shadow-sm d-zoom-2">
                                      <img alt="Alexa's avatar" src="https://i.ibb.co/CwwJsL4/init-profile.png" class="h-4 w-4" />
                                  </span>
                                  <span class="mr-25 ml-auto text-dark-l2 text-nowrap">
                                      {_school_name.school_name}
                                  </span>
                              </div>

                              <span class="mr-25 text-dark-l2 text-nowrap ">
                                ㅁㄴㅇ
                              </span>

                          </div>
                      </a>
                  </div>
                {/if}
            {/each}
        </div>
    </div>
  </div>

  <br>

  <!-- 페이징처리 시작 -->
  <ul class="pagination justify-content-center">
    <!-- 이전페이지 -->
    <li class="page-item {$search_school_page <= 1 && 'disabled'}">
        <button class="page-link" on:click="{() => search_result(site_search_text,$search_school_page-1)}">이전</button>
    </li>
    <!-- 페이지번호 -->
    {#each Array(total_page+1) as _, loop_page}
      {#if loop_page!=0} 
        <li class="page-item {loop_page === $search_school_page && 'active'}">
          <button on:click="{() => search_result(site_search_text,loop_page)}" class="page-link">{loop_page}</button>
        </li>
      {/if}
    {/each}
    <!-- 다음페이지 -->
    <li class="page-item {$search_school_page >= total_page && 'disabled'}">
        <button class="page-link" on:click="{() => search_result(site_search_text,$search_school_page+1)}">다음</button>
    </li>
  </ul>
  <!-- 페이징처리 끝 -->
  
</div>
