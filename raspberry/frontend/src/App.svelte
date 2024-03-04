<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import User from "./routes/User.svelte"
  import Rank from './routes/Rank.svelte'
  import Record_Detail from './routes/Record_Detail.svelte'
  import Game from './routes/Game.svelte'
  import UserSetting from './routes/User_setting.svelte'
  

  const routes = {
    '/': Home,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/profile/:school_number/log/:record_id': Detail,
    '/profile/:school_number' : User,
    '/profile/:school_number/Record-Detail/:category':Record_Detail,
    '/rank' : Rank,
    '/game' : Game,
    '/profile/:school_number/setting':UserSetting,

    
    /*
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,
    */
  }
</script>

<Navigation />
<Router {routes}/>