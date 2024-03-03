<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push,link } from 'svelte-spa-router'
    import { is_login, school_number ,rank_category_page} from "../lib/store"
    import {MAIN_CATEGORY} from "../lib/category"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    const emojis = {
        "1st" : "🥇",
        "2nd" : "🥈",
        "3rd"  : "🥉",
        "no_medal" : ""
    }

    /*export let params = {}*/
    let page_data_cnt = 10
    let now_page = 1
    let rank_list = []
    let class_rank_list = []
    let user_rank = {}
    let my_class = 0
    if($is_login){
        my_class=parseInt(($school_number)/100)%10
    }else{
        my_class=1
    }

    if($rank_category_page==""){
        $rank_category_page="수열"
    }
    
    function get_rank_all(category) {
        let params = {
            category : category
        }
        fastapi("get", "/api/rank/list/" + page_data_cnt + "/" + now_page, params, (json) => {
            
            rank_list = json.rank_list
            $rank_category_page=category
        })
    }
    function get_rank_class(_class,category) {
        let params = {
            category : category
        }
        fastapi("get", "/api/rank/class/list/" + _class, params, (json) => {
            
            class_rank_list = json.rank_list
            for(const [index, all_rank] of class_rank_list.entries()){
                users_rank(all_rank.user_id,index,category)

            }
        })
    }

    function users_rank(school_number,index,category) {
        let value=0
        fastapi("get", "/api/rank/user-profile/" + school_number + "/" + category, {}, (json) => {
            value=json.rank
            if(value!=0){

                if(value==-1){
                    user_rank[index] = "999+"
                }else{
                    user_rank[index] = value
                }
            }


        })
    }
    function scoreboard_update(_rank_category_page){
        get_rank_all(_rank_category_page)
        get_rank_class(my_class,_rank_category_page)

    }

    $: scoreboard_update($rank_category_page)


    /*get_score($school_number)*/

</script>



<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" />
<div class="container">
    <div class="row">
        <div class="col-sm-5 mr-0">
            <div class="card ccard radius-t-0 h-100">
                <div class="position-tl w-102 border-t-3 brc-primary-tp3 ml-n1px mt-n1px"></div>
                <div class="card-header pb-3 brc-secondary-l3">
                    <h5 class="card-title mb-2 mb-md-0 text-dark-m3 text-center">
                        {$rank_category_page} 랭킹
                    </h5>
                </div>
                {#each rank_list as rank, i}
                    <div class="card-body pt-2 pb-1">
                        <a href="/#/profile/{rank.user_id}/" style="text-decoration:none; color:black">
                            <div role="button" class="d-flex flex-wrap align-items-center my-2 bgc-secondary-l4 bgc-h-secondary-l3 radius-1 p-25 d-style">
                                <span class="mr-25 w-4 text-center" style="font-size: 27px">
                                    {#if page_data_cnt*(now_page-1)+i+1==1}
                                        {emojis["1st"]}
                                    {:else if page_data_cnt*(now_page-1)+i+1==2}
                                        {emojis["2nd"]}
                                    {:else if page_data_cnt*(now_page-1)+i+1==3}
                                        {emojis["3rd"]}
                                    {/if}
                                </span>
                                <span class="mr-25 w-5 text-center">
                                    {page_data_cnt*(now_page-1)+i+1}
                                </span>
                                <span class="mr-25 w-4 h-4 overflow-hidden text-center border-1 brc-secondary-m2 radius-round shadow-sm d-zoom-2">
                                    <img alt="Alexa's avatar" src="https://i.ibb.co/CwwJsL4/init-profile.png" class="h-4 w-4" />
                                </span>
                                <span class="mr-25 ml-auto text-dark-l2 text-nowrap">
                                    {rank.user_name}({rank.user_id})
                                </span>
                                <nav>
                                    <span class="mr-25 text-dark-l2 text-nowrap ">
                                        {rank.score}점
                                    </span>
                                </nav>
                            </div>
                        </a>
                    </div>
                {/each}
            </div>
        </div>
        {#if $is_login}
            <div class="col-sm-5 mr-0">
                <div class="card ccard radius-t-0 h-100">
                    <div class="position-tl w-102 border-t-3 brc-primary-tp3 ml-n1px mt-n1px"></div>
                    <div class="card-header pb-3 brc-secondary-l3">
                        <h5 class="card-title mb-2 mb-md-0 text-dark-m3 text-center">
                            {my_class}반 랭킹
                        </h5>
                    </div>
                    {#each class_rank_list as rank, i}
                        <div class="card-body pt-2 pb-1">
                            <a href="/#/profile/{rank.user_id}/" style="text-decoration:none; color:black">
                                <div role="button" class="d-flex flex-wrap align-items-center my-2 bgc-secondary-l4 bgc-h-secondary-l3 radius-1 p-25 d-style">
                                    <span class="mr-25 w-4 text-center" style="font-size: 27px">
                                        {#if page_data_cnt*(now_page-1)+i+1==1}
                                            {emojis["1st"]}
                                        {:else if page_data_cnt*(now_page-1)+i+1==2}
                                            {emojis["2nd"]}
                                        {:else if page_data_cnt*(now_page-1)+i+1==3}
                                            {emojis["3rd"]}
                                        {/if}
                                    </span>
                                    <span class="mr-40 w-5 text-center">
                                        {page_data_cnt*(now_page-1)+i+1}({user_rank[i]})
                                    </span>
                                    <span class="mr-25 w-4 h-4 overflow-hidden text-center border-1 brc-secondary-m2 radius-round shadow-sm d-zoom-2">
                                        <img alt="Alexa's avatar" src="https://i.ibb.co/CwwJsL4/init-profile.png" class="h-4 w-4" />
                                    </span>
                                    <span class="mr-25 ml-auto text-dark-l2 text-nowrap">
                                        {rank.user_name}({rank.user_id})
                                    </span>
                                    <nav>
                                        <span class="mr-25 text-dark-l2 text-nowrap ">
                                            {rank.score}점
                                        </span>
                                    </nav>
                                </div>
                            </a>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>
    <ul class="pagination justify-content-center">
        <!-- 페이지번호 -->
        {#each MAIN_CATEGORY as sub_category,i}
            <li class="page-item {(sub_category==$rank_category_page) && "active"}">
                <button on:click="{() => scoreboard_update(sub_category)}" class="page-link">{sub_category}</button>
            </li>
        {/each}
    </ul>
</div>