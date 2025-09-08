<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let username = ''
    let school_number = 0
    let school_name = ''
    let password1 = ''
    let password2 = ''

    function post_user(event) {
        //console.log('!!!')
        //console.log(school_number)
        event.preventDefault()
        let url = "/api/user/create"
        let params = {
            username: username,
            school_name : school_name,
            school_number : school_number,
            password1: password1,
            password2: password2,
        }
        fastapi('post', url, params, 
            (json) => {
                push('/user-login/'+school_name) /* 만약 수행이 정상적으로 되면, push 안의 링크로 이동*/
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <div class="container bootstrap snippets bootdey">      
        <div class="" style="min-height:400px;height:auto;">
            <div class="col-md-10 col-md-offset-2 login_center">
                <form class="form-horizontal">
                    <div class=" jumbotron text-center form-group text-center">
                        <div class="col-sm-10 reg-icon login_center">
                            <span class="fa fa-user fa-3x"> Sign up</span>
                        </div>
                    </div>
                    <br>
                    <Error error={error} />
                    <div class="form-group">
                        <label for="school_name">
                            <div class="login_text">
                                <b>학교 이름</b>
                            </div>
                        </label> <!--school_name id 라는 값을 가진애랑 묶여 있음-->
                        <div class="col-sm-20 login_center login_border">
                            <input type="text" class="form-control " id="school_name" bind:value="{school_name}" placeholder="학교 이름을 입력해주세요">
                        </div>
                    </div>
                    <br>
                    <div class="form-group">
                        <label for="Username">
                            <div class="login_text">
                                <b>사용자 이름</b>
                            </div>
                        </label>
                        <div class="col-sm-20 login_center login_border">
                        <input type="text" class="form-control" id="Username" bind:value="{username}" placeholder="이름을 입력해주세요">
                        </div>
                    </div>
                    <br>
                    <div class="form-group">
                        <label for="Userschoolnumber">
                            <div class="login_text">
                                <b>사용자 학번</b>
                            </div>
                        </label>
                        <div class="col-sm-20 login_center login_border">
                        <input type="number" class="form-control" id="Userschoolnumber" bind:value="{school_number}" placeholder="학번을 입력해주세요">
                        </div>
                    </div>
                    <br>
                    <div class="form-group">
                        <label for="password1">
                            <div class="login_text">
                                <b>비밀번호</b>
                            </div>
                        </label>
                        <div class="col-sm-20 login_center login_border">
                        <input type="password" class="form-control" id="password1" bind:value="{password1}" placeholder="비밀번호를 입력해주세요">
                        </div>
                    </div>
                    <br>
                    <div class="form-group">
                        <label for="password2">
                            <div class="login_text">
                                <b>비밀번호 확인</b>
                            </div>
                        </label>
                        <div class="col-sm-20 login_center login_border">
                        <input type="password" class="form-control" id="password2" bind:value="{password2}" placeholder="비밀번호를 한번 더 입력해주세요">
                        </div>
                    </div>
                    <br>

                    <div class="form-group">
                        <div class="col-sm-20 login_center ">
                        <button type="submit" class="btn btn-info" on:click="{post_user}">
                            <span class="glyphicon glyphicon-share-alt"></span>
                                <b>Register</b>
                        </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>       
</div>