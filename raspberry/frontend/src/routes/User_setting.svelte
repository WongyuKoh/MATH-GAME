<!--
argon2.exceptions.VerifyMismatchError: The password does not match the supplied hash
에러는 로그인 실패시 뜨는에러
-->


<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"    
    import { } from "../lib/store"

    export let params = {}
    let error = {detail:[]}
    let school_number = params.school_number
    let username = ""
    let change_new_password = ""
    let change_password=0

    function USERNAME(){
        fastapi("get", "/api/user/username/" + school_number, {}, (json) => {
            username=json.username
        })
    }

    function CHANGE_PASSWORD(event){
        event.preventDefault()

        let _params = {
            new_password : change_new_password
        }

        fastapi("change", "/api/user/password-change/" + school_number, _params, (json) => {
            change_password=1
        },
        (json_error) => {
            error = json_error
        })
    }

    USERNAME()
    
</script>

<div class="container">

    <div class="d-flex justify-content-center">
        <div class="col-md-3 mb-3"><!-- md : 가로 사이즈, mb : 세로 사이즈-->
            <div class="card card-body">
                <div class="d-flex flex-column align-items-center text-center">
                    <img src="https://i.ibb.co/CwwJsL4/init-profile.png" alt="Admin" class="rounded-circle" width="150">
                    <div class="mt-3">
                        <h5>{username}({school_number})</h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <Error error={error} />
    {#if change_password}
        <div class="alert alert-success" role="alert">
            <div>
                <b>변경 완료</b>
            </div>
        </div>
    {/if}
    <div class="my-3 border-bottom pb-2"></div>
    <form method="post">
        <div class="mb-3">
            <label for="password"><h6>비밀번호 변경(hash 알고리즘을 사용하였기에 기존 비밀번호를 불러올 수 없습니다.)</h6></label>
            <input type="text" class="form-control" id="password" bind:value="{change_new_password}">
        </div>

        <button type="submit" class="btn btn-primary" on:click="{CHANGE_PASSWORD}">변경</button>
    </form>
</div>