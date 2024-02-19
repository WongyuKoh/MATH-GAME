<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push,link } from 'svelte-spa-router'
    import { school_number,is_login,username } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    /*'/profile/:school_number/log/:record_id/': Detail,*/
    export let params = {}
    let record_id = params.record_id
    let record_detail_list = []


    function get_question() {
        fastapi("get", "/api/detail/" + record_id, {}, (json) => {
            record_detail_list = json.detail

        })
    }
    $: get_question()

</script>

<div class="container my-3">
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>문제</th>
            <th>카테고리</th>
            <th>문제 답</th>
            <th>{$username}의 답</th>
        </tr>
        </thead>
        <tbody>
            {#each record_detail_list as detail, i}
            <tr class="text-center">
                <td>{detail.problem}</td> 
                <td>{detail.category}</td>
                <td>{detail.problem_answer}</td>
                <td>{detail.user_answers}</td>
                <!--<td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>-->
            </tr>
            {/each}
        
    </table>
</div>
<!--
<h1>{question.subject}</h1>
<div>
    {question.content}
</div>
<ul>
    {#each question.answers as answer}
        <li>{answer.content}</li>
    {/each}
</ul>
<Error error={error} />

<form method="post">
    <textarea rows="15" bind:value={content}></textarea>
    <input type="submit" value="답변등록" on:click="{post_answer}">
</form>

<style>
    textarea {
        width:100%;
    }
    input[type=submit] {
        margin-top:10px;
    }    
</style>
-->