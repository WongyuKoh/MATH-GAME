
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
        //console.log(MAIN_CATEGORY)


      })

    }
    function user_score(category){
        let params = {
            category:category,
            school_number : $school_number
        }
        fastapi("get", "/api/user/score", params, (json) => {

            category_rank[category] = json.score
            //console.log('!!!',category_rank[category])


        })

    }

    gametype_list()
</script>

<div class="container">
    <div class="main-body d-flex justify-content-center">
        <div class="col-md-10">
            <br>
            <h5 class="text-center"><b>GAMEMODE</b></h5>
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