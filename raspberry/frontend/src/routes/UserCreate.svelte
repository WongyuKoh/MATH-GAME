<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let username = ''
    let school_number = 0
    let password1 = ''
    let password2 = ''

    function post_user(event) {
        event.preventDefault()
        let url = "/api/user/create"
        let params = {
            username: username,
            school_number : school_number,
            password1: password1,
            password2: password2,
        }
        fastapi('post', url, params, 
            (json) => {
                push('/user-login') /* 만약 수행이 정상적으로 되면, push 안의 링크로 이동*/
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <div class="main-body d-flex justify-content-center">
        <div class="col-md-10">
            <div class="card text-center">
                <h3><b>학번은 2024학년도 2학년 학번으로 해주세요.</b></h3>
            </div>
        </div>
    </div>
    <h5 class="my-3 border-bottom pb-2">회원 가입</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" id="username" bind:value="{username}">
        </div>
        <div class="mb-3">
            <label for="username">사용자 학번</label>
            <input type="text" class="form-control" id="school_number" bind:value="{school_number}">
        </div>
        <div class="mb-3">
            <label for="password1">비밀번호</label>
            <input type="password" class="form-control" id="password1" bind:value="{password1}">
        </div>
        <div class="mb-3">
            <label for="password2">비밀번호 확인</label>
            <input type="password" class="form-control" id="password2" bind:value="{password2}">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{post_user}">생성하기</button>
    </form>
</div>