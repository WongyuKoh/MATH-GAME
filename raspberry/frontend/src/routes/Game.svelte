
<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push,link } from 'svelte-spa-router'
    import { is_login,school_number,school_name } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    import { slide } from "svelte/transition";
    moment.locale('ko')

    let MAIN_CATEGORY = []
    let gametypelist = []
    let category_rank = []


    function gametype_list(){
      fastapi("get", "/api/gametype/type-list", {}, (json) => {

        gametypelist=json.gametype_list
        MAIN_CATEGORY = []
        //console.log('gametypelist : ',gametypelist)

        for(const gametype of gametypelist){
          MAIN_CATEGORY.push(gametype.typename)
          user_score(gametype.typename)
        }
        console.log(MAIN_CATEGORY)


      })

    }
    function user_score(category){
        let params = {
            category:category,
            school_number : $school_number
        }
        fastapi("get", "/api/user/score", params, (json) => {

            category_rank[category] = json.score
            console.log('!!!',category_rank[category])


        })

    }



    gametype_list()



</script>


<div class="container">
    <div class="main-body d-flex justify-content-center">
        <div class="col-md-10">
            <h5 class="text-center"><b>GAMERULE</b></h5>
            <div class="card text-center">
                <div class="card-body">
                    이 게임은 수학과 두더지 게임이 융합된 게임입니다.
                    <br>
                    <br>
                    게임 룰은 기존 두더지 게임과 동일하게 두더지를 때리면 되는 게임입니다.
                    <br>
                    <br>
                    하지만 기존과는 다르게 상단에 문제가 주어지며, 문제에 대한 답을 들고 있는 두더지를 때려야지 점수가 올라갑니다.
                    <br>
                    <br>
                    올바르지 않은 정답을 들고 있는 두더지를 때리면 점수가 깎이며, 각 문제 유형별로 점수의 분포가 다르게 적용됩니다.
                    <br>
                    <br>
                    최종 결과는 게임이 끝나면 확인할 수 있으며, 
                    <br>
                    <br>
                    해당 사이트에서 본인 이름으로 로그인하거나 홈에서 본인 학번과 이름을 찾으신다음 들어가시면 확인하실 수 있습니다.

                    <br>
                    <br>

                    <!-- "두더지 때리기 게임에 오신걸 환영합니다!!\n\n"+\
                    "두더지 때리기 게임은 기존 두더지 때리기 게임처럼 \n\n"+\
                    "두더지가 올라왔을 때 때리면 되는 간단한 게임입니다. \n\n\n "+\
                    "하지만 기존과 다르게 \n\n 두더지가 들고 올라오는 칠판에 숫자가 쓰여있습니다. \n\n\n"+\
                    "칠판에 쓰여져 있는 숫자는 \n\n상단 보드판에 나타난 문제에 대한 답입니다.\n\n"+\
                    "상단 보드판에는 등차수열의 형태로 나타나게 되는데, \n\n"+\
                    "그중 □ 가 있는 곳에 들어갈 숫자를 골라주시면 됩니다. \n\n\n\n"+\
                    "등차수열이란?\n\n"+\
                    "첫번째항부터 차례로 일정한 수를 더하여 \n\n 만들어지는 수열을 말합니다.\n\n"+\
                    "이때 첫번째 항을 초항, \n\n 더하는 일정한 수를 공차라고 합니다.\n\n"+\
                    "이정도 내용을 숙지하고 이제 게임을 즐겨봅시다!!" 
                    
                    http://127.0.0.1:5501/?token=20402&type=%EC%A7%80%EC%88%98&school=%EC%9A%B4%ED%98%B8%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90
                    https://python-programmer1512.github.io/WHACK-THE-MOLE.github.io/?token={school_number}&type={category}&school={school_name}
                    -->

                
                </div>
            </div>
            <section id="pricing" class="pricing-content section-padding">
                <div class="container">			
                    <br>			
                    <div class="row text-center">		
                        {#each MAIN_CATEGORY as category_name,i}								
                            <div class="col-lg-4 col-sm-6 col-xs-12 wow fadeInUp" data-wow-duration="1s" data-wow-delay="0.1s" data-wow-offset="0" style="visibility: visible; animation-duration: 1s; animation-delay: 0.1s; animation-name: fadeInUp;">
                                <div class="pricing_design">
                                    <div class="single-pricing">
                                        <div class="price-head">		
                                            <h2>{category_name}</h2>
                                        </div>
                                        <ul>
                                            <b><li>최고 점수 : {category_rank[category_name]}점</li></b>
                                        </ul>
                                        <div class="pricing-price">
                                            
                                        </div>
                                        <a href="https://python-programmer1512.github.io/WHACK-THE-MOLE.github.io/?token={$school_number}&type={category_name}&school={$school_name}" class="price_btn"><b>Game Play</b></a>
                                    </div>
                                </div>
                            </div><!--- END COL -->	
                        {/each}	  
                    </div><!--- END ROW -->
                </div><!--- END CONTAINER -->
            </section>
        </div>
    </div>
</div>