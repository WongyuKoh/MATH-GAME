<script>/* script 부분은 처음에 한번만 실행함, 대신 $: 는 계속 실행함*/
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import moment from 'moment/min/moment-with-locales'
    import { sub_category_page,record_page  } from "../lib/store"
    moment.locale('ko')

    export let params = {}
    let school_number = params.school_number

    let records=[]

    let record_list = []
    
    let total_page = 0
    let one_page_cnt = 10

    let MAIN_CATEGORY = []
    let gametypelist = []
    fastapi("get", "/api/gametype/type-list", {}, (json) => {
        gametypelist=json.gametype_list
        MAIN_CATEGORY = []
        for(const gametype of gametypelist){
            MAIN_CATEGORY.push(gametype.typename)
        }
        total_page = MAIN_CATEGORY.length

    })

    function get_record_recent(page){
        let _params = {
            page : page,
            cnt : one_page_cnt
        }
        fastapi("get", "/api/user/detail-limit/" + school_number, _params, (json) => {
            records=json.records
            //console.log(json.records)
            $record_page = page
            total_page = Math.floor(json.records_cnt/one_page_cnt)
            if(json.records_cnt % one_page_cnt !=0)total_page++

            if(total_page==0)total_page=1

        })

    }

    $:get_record_recent(1)

</script>

<div class="container my-3">
    <div class="GAME-RECORD">
        <h5><b>최근 게임 기록</b></h5>
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
                                    <a use:link href="/profile/{school_number}/log/{recent_record.id}">자세히 보기</a>
                                </td>
                        {/each}
                    </tbody>
                </table>   
            </div>
        </div>
    </div>


    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$record_page <= 1 && 'disabled'}">
            <button class="page-link" on:click="{() => get_record_recent($record_page-1)}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page+1) as _, loop_page}
        {#if loop_page!=0} 
            <li class="page-item {loop_page === $record_page && 'active'}">
            <button on:click="{() => get_record_recent(loop_page)}" class="page-link">{loop_page}</button>
            </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$record_page >= total_page && 'disabled'}">
            <button class="page-link" on:click="{() => get_record_recent($record_page+1)}">다음</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->


</div>
