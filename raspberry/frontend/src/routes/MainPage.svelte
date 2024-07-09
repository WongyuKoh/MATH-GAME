<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { school_class,is_login, access_token, username, school_number  } from "../lib/store"
    import {MAIN_CATEGORY} from "../lib/category"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('en')
    let search_text = ""

    console.log($is_login)

    function func(e){
      switch(e.keyCode) {
		    case 13:
          window.location.href = '/#/search/'+search_text;
				  break;
		  }
    }
    /* 
    $: 는 svelte 에서 반응형 을 의미함, 즉 api 호출이 있으면 바뀐 total과 size에 대해 total_page를 구한다
    */
    /* $가 변수 앞에 변수 앞에 붙는 이유는 다른 변수들과의 이름이 중복되지 않도록, 잘쓰지 않는 기호를 앞에 붙여준거*/

  </script>

<!--
  https://aboooks.tistory.com/59
  tr  : table row, 가로줄 만드는거(데이터 들어가는 라인의 가장 윗부분 대로)
  th : table head , 표의 제목
  td : table data, 셀을 만드는 역할
-->

<div class="container my-3">
  {#if $is_login }
    <div>
      Hello World
    </div>

  {:else}
    <div class="SCREEN">

      <div class="mainscreen">
        <div class="search-display">
          <a use:link href="/search/{search_text}"> <!-- 잘 작동함-->
            <img src="../image/search_blue.svg" alt="" class="search-button" width="45">
          </a>
          
          <input type="text" class="school-search" id="username" bind:value="{search_text}" on:keydown|preventDefault={func} placeholder="학교명을 검색하세요.">
          
          
        
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
  