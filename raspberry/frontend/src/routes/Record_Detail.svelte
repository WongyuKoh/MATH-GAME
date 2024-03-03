<script>/* script 부분은 처음에 한번만 실행함, 대신 $: 는 계속 실행함*/
  import fastapi from "../lib/api"
  import { link } from 'svelte-spa-router'
  import moment from 'moment/min/moment-with-locales'
  import {MAIN_CATEGORY} from "../lib/category"
  import { sub_category_page  } from "../lib/store"
  moment.locale('ko')

  export let params = {}
  let school_number = params.school_number
  let category = params.category

  let record_list = []
  const total_page = MAIN_CATEGORY.length
  /* 
  $: 는 svelte 에서 반응형 을 의미함, 즉 api 호출이 있으면 바뀐 total과 size에 대해 total_page를 구한다
  */
  /* $가 변수 앞에 변수 앞에 붙는 이유는 다른 변수들과의 이름이 중복되지 않도록, 잘쓰지 않는 기호를 앞에 붙여준거*/
  function get_record_list(sub_category) {
      fastapi("get", "/api/record/record-by-category-all/" + school_number+"/"+sub_category, {}, (json) => {
        record_list = json.record_list
        $sub_category_page = sub_category

      })

  }

  $: get_record_list(category)
</script>

<!--
https://aboooks.tistory.com/59
tr  : table row, 가로줄 만드는거(데이터 들어가는 라인의 가장 윗부분 대로)
th : table head , 표의 제목
td : table data, 셀을 만드는 역할
-->
<div class="container my-3">
    <div class="GAME-RECORD">
        <h5><b>{$sub_category_page}</b></h5>
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

                        {#each record_list as record, i}
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
                                    <a use:link href="/profile/{school_number}/log/{record.id}/">자세히 보기</a>
                                </td>
                        {/each}
                    </tbody>
                </table>   
            </div>
        </div>
    </div>
    <ul class="pagination justify-content-center">
        <!-- 페이지번호 -->
        {#each MAIN_CATEGORY as sub_category,i}
            <li class="page-item {(sub_category==$sub_category_page) && "active"}">
                <button on:click="{() => get_record_list(sub_category)}" class="page-link">{sub_category}</button>
            </li>
        {/each}
    </ul>


</div>
