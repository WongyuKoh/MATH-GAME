/*
https://velog.io/@devp1023/JS-%EC%A1%B0%EA%B1%B4-%EC%B2%98%EB%A6%AC-IF#5-%EC%A1%B0%EA%B1%B4%EB%AC%B8-%EC%97%B0%EC%82%B0%EC%9E%90-
? 내용
(조건문) ? A : B 이면, 조건문이 참이라면 A, 거짓이라면 B를 실행하는 코드 둘중에 하나가 없을 수 있음
문자를 숫자로 읽기 : parse
숫자를 문자로 읽기 : stringify

https://hianna.tistory.com/697
localStorage 사용법
*/


import { writable } from 'svelte/store'

const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)

    const store = writable((storedValueStr != null && storedValueStr != "undefined")? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const rank_category_page = persist_storage("rank_category_page","수열")
export const sub_category_page = persist_storage("sub_category_page", "")
export const school_class = persist_storage("school_class", 1)
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)
export const school_number = persist_storage("school_number", '11111')