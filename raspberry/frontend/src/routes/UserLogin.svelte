<!--
argon2.exceptions.VerifyMismatchError: The password does not match the supplied hash
에러는 로그인 실패시 뜨는에러
-->


<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"    
    import { access_token, username, is_login, school_number } from "../lib/store"

    let error = {detail:[]}
    let login_username = ""
    let login_password = ""

    function login(event) {
        event.preventDefault()
        let url = "/api/user/login"
        let params = {
            username: login_username,
            password: login_password,
        }
        /*
        return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "school_number": user.school_number
         }
         
        */
        fastapi('login', url, params, 
            (json) => {
                $access_token = json.access_token
                $username = json.username
                $school_number = json.school_number

                $is_login = true
                push("/")
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">

    <h5 class="my-3 border-bottom pb-2">로그인</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" id="username" bind:value="{login_username}">
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control" id="password" bind:value="{login_password}">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{login}">로그인</button>
    </form>
</div>