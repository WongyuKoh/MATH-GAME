<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push,link } from 'svelte-spa-router'
    import { is_login, school_number } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    const emojis = {
        "first" : "🥇",
        "second" : "🥈",
        "thrid"  : "🥉",
        "no_medal" : ""
    }

    /*export let params = {}*/
    let page_data_cnt = 10
    let now_page = 1
    let rank_list = []
    let class_rank_list = []
    let user_rank = {}
    let my_class = parseInt(($school_number)/100)%10
    
    function get_rank_all() {
        fastapi("get", "/api/rank/list/" + page_data_cnt + "/" + now_page, {}, (json) => {
            
            rank_list = json.rank_list
        })
    }
    function get_rank_class(_class) {
        fastapi("get", "/api/rank/class/list/" + _class, {}, (json) => {
            
            class_rank_list = json.rank_list
            for(const [index, all_rank] of class_rank_list.entries()){
                users_rank(all_rank.user_id,all_rank.score,index)

            }
        })
    }

    function users_rank(school_number,score,index) {
        let params = {
            score : score
        }

        let value=0
        fastapi("get", "/api/rank/user/" + school_number, params, (json) => {
            value=json.rank
            if(value!=0)user_rank[index] = value

        })
    }

    get_rank_all()
    get_rank_class(my_class)

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
                        전체 랭킹
                    </h5>
                </div>
                {#each rank_list as rank, i}
                    <div class="card-body pt-2 pb-1">
                        <div role="button" class="d-flex flex-wrap align-items-center my-2 bgc-secondary-l4 bgc-h-secondary-l3 radius-1 p-25 d-style">
                            <span class="mr-25 w-4 text-center" style="font-size: 27px">
                                {#if page_data_cnt*(now_page-1)+i+1==1}
                                    {emojis["first"]}
                                {:else if page_data_cnt*(now_page-1)+i+1==2}
                                    {emojis["second"]}
                                {:else if page_data_cnt*(now_page-1)+i+1==3}
                                    {emojis["thrid"]}
                                {/if}
                            </span>
                            <span class="mr-25 w-4 text-center">
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
                    </div>
                {/each}
            </div>
        </div>
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
                        <div role="button" class="d-flex flex-wrap align-items-center my-2 bgc-secondary-l4 bgc-h-secondary-l3 radius-1 p-25 d-style">
                            <span class="mr-25 w-4 text-center" style="font-size: 27px">
                                {#if page_data_cnt*(now_page-1)+i+1==1}
                                    {emojis["first"]}
                                {:else if page_data_cnt*(now_page-1)+i+1==2}
                                    {emojis["second"]}
                                {:else if page_data_cnt*(now_page-1)+i+1==3}
                                    {emojis["thrid"]}
                                {/if}
                            </span>
                            <span class="mr-40 w-4 text-center">
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
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>