
<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push,link } from 'svelte-spa-router'
    import { is_login } from "../lib/store"
    import {MAIN_CATEGORY} from "../lib/category"
    import moment from 'moment/min/moment-with-locales'
    import { slide } from "svelte/transition";
    moment.locale('ko')



</script>


<div class="container">
    <div class="main-body d-flex justify-content-center">
        <div class="col-md-10">
            <h5 class="text-center"><b>게임 룰</b></h5>
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
                    "이정도 내용을 숙지하고 이제 게임을 즐겨봅시다!!" -->

                    <a href="https://python-programmer1512.github.io/WHACK-THE-MOLE.github.io/" class="btn btn-primary">게임 하러가기</a>
                </div>
            </div>
        </div>
    </div>
</div>