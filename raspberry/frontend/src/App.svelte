<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import MainPage from "./routes/MainPage.svelte"
  import Detail from "./routes/Detail.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import User from "./routes/User.svelte"
  import Rank from './routes/Rank.svelte'
  import Record_Detail from './routes/Record_Detail.svelte'
  import Game from './routes/Game.svelte'
  import UserSetting from './routes/User_setting.svelte'
  import Search from './routes/Search.svelte'

  const routes = {
    '/': MainPage,
    '/home':Home,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/profile/:school_number/log/:record_id': Detail,
    '/profile/:school_number' : User,
    '/profile/:school_number/Record-Detail/:category':Record_Detail,
    '/rank' : Rank,
    '/game' : Game,
    '/profile/:school_number/setting':UserSetting,
    '/search/:search_text' : Search

    
    /*
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,

    https://blog37.tistory.com/entry/%EC%8A%A4%EB%B2%A8%ED%8A%B8%EC%97%90%EC%84%9C-%EA%B5%AC%EA%B8%80-%EB%A8%B8%ED%8B%B0%EB%A6%AC%EC%96%BC-%EC%95%84%EC%9D%B4%EC%BD%98Google-Material-Icons-%EC%82%AC%EC%9A%A9-%EB%B0%A9%EB%B2%95
    
    구글 머티리얼 아이콘
    https://fonts.google.com/icons?selected=Material+Symbols+Outlined:search:FILL@0;wght@400;GRAD@0;opsz@24&icon.size=24&icon.color=%23e8eaed
    */
  }
</script>

<Navigation />
<Router {routes}/>


