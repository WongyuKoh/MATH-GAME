<!--
argon2.exceptions.VerifyMismatchError: The password does not match the supplied hash
에러는 로그인 실패시 뜨는에러
-->


<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"    
    import { access_token, username, is_login, school_number,school_id,school_name } from "../lib/store"

    export let params={}
    /*'/user-login/:school_name': UserLogin,*/


    let error = {detail:[]}
    let login_username = ""
    let login_password = ""
    let login_school_name = ""

    if(params.school_name=="none"){
        login_school_name = ""
    }else{
        login_school_name = params.school_name
    }
    //console.log('!@!@!')
    //console.log(login_school_name)

    function login(event) {
        
        //console.log('!2222@!@!')
        //console.log(login_school_name)
        event.preventDefault()
        let url = "/api/user/login"
        let params = {
            school_name:login_school_name,
            username: login_username,
            password: login_password
            
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
                $school_name = json.school_name
                $school_id = json.school_id

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
    <div class="container bootstrap snippets bootdey">
      
        <div class="" style="min-height:400px;height:auto;">
          <div class="col-md-10 col-md-offset-2 login_center">
              <form class="form-horizontal" role="form">
                    <div class=" jumbotron text-center form-group text-center">
                        <div class="col-sm-10 reg-icon login_center">
                            <span class="fa fa-user fa-3x"> Sign in</span>
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
                            <input type="text" class="form-control " id="school_name" bind:value="{login_school_name}" placeholder="학교 이름을 입력해주세요">
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
                        <input type="text" class="form-control" id="Username" bind:value="{login_username}" placeholder="이름을 입력해주세요">
                        </div>
                    </div>
                    <br>
                    <div class="form-group">
                        <label for="password">
                            <div class="login_text">
                                <b>비밀번호</b>
                            </div>
                        </label>
                        <div class="col-sm-20 login_center login_border">
                        <input type="password" class="form-control" id="password" bind:value="{login_password}" placeholder="비밀번호를 입력해주세요">
                        </div>
                    </div>
                    <br>

                    <div class="form-group">
                        <div class="col-sm-20 login_center ">
                        <button type="submit" class="btn btn-info" on:click="{login}">
                            <span class="glyphicon glyphicon-share-alt"></span>
                            <b>Login</b>
                        </button>
                        </div>
                    </div>
              </form>
          </div>
        </div>
      </div>               

    <!-- <h5 class="my-3 border-bottom pb-2">로그인</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">사용자 학교</label>
            <input type="text" class="form-control" id="schoolname" bind:value="{login_school_name}" placeholder="enter your school name">
        </div>
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" id="username" bind:value="{login_username}" placeholder="enter your name">
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control" id="password" bind:value="{login_password}" placeholder="enter your password">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{login}">로그인</button>
    </form> -->
</div>