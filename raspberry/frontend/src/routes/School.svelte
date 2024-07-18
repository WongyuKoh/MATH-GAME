<!--
argon2.exceptions.VerifyMismatchError: The password does not match the supplied hash
에러는 로그인 실패시 뜨는에러
-->


<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"    
    import { access_token, username, is_login, school_number,school_id } from "../lib/store"

    /*'/user-login/:school_name': UserLogin,*/


    let error = {detail:[]}
	let school_name = ''
	let school_address = ''
    //console.log('!@!@!')
    //console.log(login_school_name)
	function school_register(){

		let params = {
			school_name : school_name,
			school_address : school_address
		}

		fastapi("school_post", "/api/school/create", params, (json) => {
            push("/")
        },
		(json_error) => {
                error = json_error
            })

	}
</script>

<div class="container">
    <div class="container bootstrap snippets bootdey">
      
        <div class="" style="min-height:400px;height:auto;">
          <div class="col-md-10 col-md-offset-2 login_center">
              <form class="form-horizontal" role="form">
                    <div class=" jumbotron text-center form-group text-center">
                        <div class="col-sm-10 reg-icon login_center">
                            <span class="fa fa-user fa-3x"> School Register</span>
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
                                <b>학교 주소</b>
                            </div>
                        </label>
                        <div class="col-sm-20 login_center login_border">
                        <input type="text" class="form-control" id="Username" bind:value="{school_address}" placeholder="학교 주소를 입력해주세요">
                        </div>
                    </div>
                    <br>

                    <div class="form-group">
                        <div class="col-sm-20 login_center ">
                        <button type="submit" class="btn btn-info" on:click="{school_register}">
                            <span class="glyphicon glyphicon-share-alt"></span>
                            <b>Register</b>
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