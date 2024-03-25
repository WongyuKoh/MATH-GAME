<script>
    import { link } from 'svelte-spa-router'
    import { school_class,access_token, username, is_login, school_number } from "../lib/store"
</script>

<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/" on:click="{() => {$school_class = 0}}">Math Game</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" />
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="me-auto" />
            <ul class="navbar-nav ml-auto mb-2 mb-lg-0">
                {#if $is_login }
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/rank">랭킹</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/game">게임</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-login" on:click={() => {
                            $access_token = ''
                            $username = ''
                            $school_number = '11111'
                            $is_login = false
                        }}>로그아웃 </a>
                        
                    </li>
                    <li class="nav-item">


                        <a use:link class="nav-link" href="/profile/{$school_number}/">
                            {$username}({$school_number})
                        </a>

                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/rank">랭킹</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-create">회원가입</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-login">로그인</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>