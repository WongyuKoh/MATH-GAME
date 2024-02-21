<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import User from "./routes/User.svelte"
  import Rank from './routes/Rank.svelte';

  

  const routes = {
    '/': Home,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/profile/:school_number/log/:record_id/': Detail,
    '/profile/:school_number' : User,
    '/rank' : Rank
    
    /*
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,
    */
  }
</script>

<Navigation />
<Router {routes}/>