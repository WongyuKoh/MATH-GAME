const cursor = document.querySelector('.cursor')
const holes = [...document.querySelectorAll('.mole')]
const hole_out = new Array(holes.length).fill(0);
const scoreEl = document.querySelector('.score span')
const TIMER=document.querySelector('.timer span');
let score = 0



function rand(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

function game_start(){
    for(var i=0;i<holes.length;i++){
        const hole = holes[i]
        const img = document.createElement('img')
        img.classList.add('mole-down')
        img.src = './image/mole.png'
        img.id = 'mole-movement_'+i
        
        hole.appendChild(img)

        const span = document.createElement('span')
        let mole_text=document.createTextNode('a')
        span.classList.add('text-down')
        span.appendChild(mole_text)
        span.id = 'text-movement_'+i

        hole.appendChild(span)



    }
}

function mole_move(A,B,i){ /* class : A -> B, down : {A:mole-rise,B:mole-down}, up : {A:mole-down,B:mole-rise} */
    const mole_before_class = "mole-"+A
    const mole_after_class = "mole-"+B

    const text_before_class = "text-"+A
    const text_after_class = "text-"+B

    const before_class = document.getElementById("mole-movement_"+i)
    before_class.classList.replace(mole_before_class,mole_after_class)

    const before_class_text = document.getElementById("text-movement_"+i)
    before_class_text.classList.replace(text_before_class,text_after_class)


}

function updateTimer() {
    const future = Date.parse("2024/01/01 00:00:00")
    const now = new Date()
    const diff = future - now

    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const mins = Math.floor(diff / (1000 * 60))
    const secs = Math.floor(diff / 1000)

    const d = days
    const h = hours - days * 24
    const m = mins - hours * 60
    const s = secs - mins * 60

    return s

}

function run(i){

    const hole = holes[i]
    let timer = null
    let uptimer = null
    TIMER.textContent = updateTimer()
    console.log(TIMER.textContent)

    uptimer = setTimeout(() => { /* 두더지가 올라오기전 대기 시간 */
        const img = document.getElementsByTagName('img')[i]
        const span = document.getElementsByTagName('span')[i]

        /* 변경 */

        span.innerHTML = "hello";
        mole_move('down','rise',i)
        hole_out[i]=1

        img.addEventListener('click', () => { /* 두더지를 때렸을 때*/
            if(hole_out[i]===1){
                hole_out[i]=0
                score += 10
                scoreEl.textContent = score
                clearTimeout(timer)
                mole_move('rise','down',i)
                run(i)
        
                setTimeout(() => {
                }, rand(1000,5000)) /* 다음 두더지가 나오는데 걸리는 시간 */
            }
        })

        hole.appendChild(img)
        hole.appendChild(span)

        timer = setTimeout  (() => { /* 두더지를 때리지 못하고 들어갔을때 */
        hole_out[i]=0
            mole_move('rise','down',i)
            run(i)
        }, rand(100000,500000))

    }, rand(1000,2000))

}
game_start()

for(var i=0;i<holes.length;i++){ /* 한번만 실행함 */
    if(hole_out[i]===0)run(i)
}

window.addEventListener('mousemove', e => {
    console.log("mousemove!!!")
    cursor.style.top = e.pageY  - cursor.clientHeight/2 + 'px'
    cursor.style.left = e.pageX - cursor.clientWidth/2 + 'px'


})
window.addEventListener('touchmove', e => {
    console.log("touchmove!!!")
    this.touches = e.changedTouches;
    cursor.style.top = this.touches[0].pageY  - cursor.clientHeight/2 + 'px'
    cursor.style.left = this.touches[0].pageX - cursor.clientWidth/2 + 'px'


})


window.addEventListener('mousedown', () => {
    console.log("MOUSEDOWN!!!")
    cursor.classList.add('active')
})
window.addEventListener('mouseup', () => {
    console.log("MOUSEUP!!!")
    cursor.classList.remove('active')
    
})

window.addEventListener('touchstart', () => {
    console.log("touchstart!!!")
    cursor.classList.add('active')
})
window.addEventListener('touchend', () => {
    console.log("touchend!!!")
    cursor.classList.remove('active')
    
})
