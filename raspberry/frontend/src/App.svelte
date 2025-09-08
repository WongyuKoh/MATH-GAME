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
  import School from './routes/School.svelte'
  import Gamerule from './routes/Gamerule.svelte'
  import UserRecord from './routes/User_Record.svelte'

  const routes = {
    '/': MainPage, /* 로그인 필요 x */
    '/home/:class':Home, /* 로그인 필요 o */
    '/user-create': UserCreate, /* 로그인 필요 x */
    '/user-login/:school_name': UserLogin, /* 로그인 필요 x */
    '/profile/:school_number/log/:record_id': Detail, /* 로그인 필요 o */
    '/profile/:school_number' : User, /* 로그인 필요 o */
    '/profile/:school_number/Record-Detail/:category':Record_Detail, /* 로그인 필요 o */
    '/rank' : Rank, /* 로그인 필요 o */
    '/game' : Game, /* 로그인 필요 o */
    '/profile/:school_number/setting':UserSetting, /* 로그인 필요 o */
    '/search/:search_text' : Search, /* 로그인 필요 x */
    '/school' : School, /* 로그인 필요 x */
    '/gamerule' : Gamerule, /* 로그인 필요 x */
    '/user-record/:school_number':UserRecord /* 로그인 필요 o */

  }
</script>

<Navigation />
<Router {routes}/>


