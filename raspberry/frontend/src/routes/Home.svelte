<script>/* script 부분은 처음에 한번만 실행함, 대신 $: 는 계속 실행함*/
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { school_class,is_login, access_token, username, school_number  } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    let user_list = []
    const total_page = 9
    /* 
    $: 는 svelte 에서 반응형 을 의미함, 즉 api 호출이 있으면 바뀐 total과 size에 대해 total_page를 구한다
    */
    /* $가 변수 앞에 변수 앞에 붙는 이유는 다른 변수들과의 이름이 중복되지 않도록, 잘쓰지 않는 기호를 앞에 붙여준거*/
    function get_user_list(_school_class) {
        let params = {
            school_class: _school_class,
        }
        fastapi('get', '/api/user/list', params, (json) => {
            user_list = json.user_list
            $school_class = _school_class

        })

    }

    $: get_user_list($school_class)

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

  </script>

<!--
  https://aboooks.tistory.com/59
  tr  : table row, 가로줄 만드는거(데이터 들어가는 라인의 가장 윗부분 대로)
  th : table head , 표의 제목
  td : table data, 셀을 만드는 역할
-->

<div class="container my-3">
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
      <tr class="text-center">
          <td>{user.school_number}</td> 
          <td>
              <a use:link href="/profile/{Number(user.school_number)}">{user.username}</a>
          </td>
          <td>{Object.keys(user.records).length}</td>
          <!--<td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>-->
      </tr>
      {/each}
      </tbody>
  </table>

  <!-- 페이징처리 시작 -->
  <ul class="pagination justify-content-center">
    <!-- 이전페이지 -->
    <li class="page-item {$school_class <= 1 && 'disabled'}">
        <button class="page-link" on:click="{() => get_user_list($school_class-1)}">이전</button>
    </li>
    <!-- 페이지번호 -->
    {#each Array(total_page+1) as _, loop_page}
      {#if loop_page!=0} 
        <li class="page-item {loop_page === $school_class && 'active'}">
          <button on:click="{() => get_user_list(loop_page)}" class="page-link">{loop_page}</button>
        </li>
      {/if}
    {/each}
    <!-- 다음페이지 -->
    <li class="page-item {$school_class >= total_page && 'disabled'}">
        <button class="page-link" on:click="{() => get_user_list($school_class+1)}">다음</button>
    </li>
  </ul>
  <!-- 페이징처리 끝 -->


</div>
  