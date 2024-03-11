<!--
argon2.exceptions.VerifyMismatchError: The password does not match the supplied hash
에러는 로그인 실패시 뜨는에러
-->


<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"    
    import { school_number  } from "../lib/store"
    import { } from "../lib/store"

    export let params = {}
    let error = {detail:[]}
    let account_school_number = params.school_number
    let username = ""
    let change_new_password = ""
    let change_password = 0
    let change_username = 0
    let change_new_username = ""
    let delete_user = 0
    let change_school_number = 0
    let change_new_school_number = 11111
    
    function USERNAME(){
        fastapi("get", "/api/user/username/" + account_school_number, {}, (json) => {
            username=json.username
        })
    }

    function CHANGE_PASSWORD(event){
        event.preventDefault()

        let _params = {
            new_password : change_new_password
        }

        fastapi("change", "/api/user/password-change/" + account_school_number, _params, (json) => {
            change_password=1
        },
        (json_error) => {
            error = json_error
        })
    }

    function CHANGE_USERNAME(event){
        event.preventDefault()

        let _params = {
            new_username : change_new_username
        }

        fastapi("change", "/api/user/username-change/" + account_school_number, _params, (json) => {
            change_username=1
        },
        (json_error) => {
            error = json_error
        })
    }

    function CHANGE_SCHOOLNUMBER(event){
        event.preventDefault()

        let _params = {
            new_school_number : change_new_school_number
        }

        fastapi("change", "/api/user/school-number-change/" + account_school_number, _params, (json) => {
            change_school_number=1
        },
        (json_error) => {
            error = json_error
        })
    }

    function DELETE_USER(){
        fastapi("post", "/api/user/school-number-delete/" + account_school_number, {}, (json) => {
            delete_user=1
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
                        <h5>{username}({account_school_number})</h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <Error error={error} />

    {#if (change_password || change_school_number || change_username) && delete_user==0 }
        <div class="alert alert-success" role="alert">
            <div>
                <b>변경 완료</b>
            </div>
        </div>
    {/if}

    {#if $school_number==202400}

        <form method="post">
            <div class="mb-3">
                <label for="school-number"><h6>학번 변경</h6></label>
                <input type="text" class="form-control" id="school-number" bind:value="{change_new_school_number}">
            </div>

            <button type="submit" class="btn btn-primary" on:click="{CHANGE_SCHOOLNUMBER}">변경</button>
        </form>

        
        <br>

    {/if}

    <div class="my-3 border-bottom pb-2"></div>
    <form method="post">
        <div class="mb-3">
            <label for="username"><h6>사용자 이름 변경</h6></label>
            <input type="text" class="form-control" id="username" bind:value="{change_new_username}">
        </div>

        <button type="submit" class="btn btn-primary" on:click="{CHANGE_USERNAME}">변경</button>
    </form>

    
    <br>


    <form method="post">
        <div class="mb-3">
            <label for="password"><h6>비밀번호 변경(hash 알고리즘을 사용하였기에 기존 비밀번호를 불러올 수 없습니다.)</h6></label>
            <input type="text" class="form-control" id="password" bind:value="{change_new_password}">
        </div>

        <button type="submit" class="btn btn-primary" on:click="{CHANGE_PASSWORD}">변경</button>
    </form>

    
    <br>

    <form method="post">
        <div class="mb-3">
            <label for="delete-uesr"><h6>계정 삭제(삭제하면 되돌릴 수 없습니다.)</h6></label>
        </div>
        <button type="submit" class="btn btn-danger" on:click="{DELETE_USER}">삭제</button>
    </form>

</div>