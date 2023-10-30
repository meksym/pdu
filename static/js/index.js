'use strict'


function setValue(listOfSugges, dots, index, value) {
    dots[index].style.opacity = value
    listOfSugges[index].style.opacity = value
    listOfSugges[index].style.zIndex = value
}

function changeSuggestion(listOfSugges, dots) {
    let i = 0
    for (let object of listOfSugges) {
        if (object.style.opacity == '1' && object.style.zIndex == '1') {
            setValue(listOfSugges, dots, i, '')
            if (i + 1 == listOfSugges.length)
                setValue(listOfSugges, dots, 0, '1')
            else
                setValue(listOfSugges, dots, i+1, '1')
            break
        }
        i += 1
    }
}

function clickDot(listOfSugges, dots) {
    return event => {
        let index = 0
        for (let point of dots) {
            if (point == event.target && point.style.opacity != '1') {
                for (let i = 0; i < listOfSugges.length; ++i)
                    setValue(listOfSugges, dots, i, '')
                setValue(listOfSugges, dots, index, '1')
                clearInterval(window.timerId)
                window.timerId = setInterval(changeSuggestion, 10000, listOfSugges, dots)
                break
            }
            index += 1
        }
    }
}

function range(stop) {
    return Array(stop).keys()
}

function rightMove(list) {
    return event => {
        let i = 0
        let amount = window.amount
        for (let object of list) {
            if (object.style.display == 'block') {
                for (let j of range(amount))
                    if (list[i + j]) list[i + j].classList.add('hide')
                setTimeout(() => {
                    for (let j of range(amount)) {
                        if (list[i + j]) list[i + j].style.display = 'none'
                        if (list[i + j]) list[i + j].classList.remove('hide', 'show')
                    }
                    let isLastRange = true
                    for (let j of range(amount))
                        if (list[i + amount + j]) isLastRange = false
                    if (isLastRange) for (let j of range(amount)) {
                        if (list[0 + j]) list[0 + j].style.display = 'block'
                        if (list[0 + j]) list[0 + j].classList.add('show')
                    } else for (let j of range(amount)) {
                        if (list[i + amount + j])
                            list[i + amount + j].style.display = 'block'
                        if (list[i + amount + j])
                            list[i + amount + j].classList.add('show')
                    }
                }, 310)
                break
            }
            i += 1
        }
    }
}

function leftMove(list) {
    return event => {
        let i = 0
        let amount = window.amount
        for (let object of list) {
            if (object.style.display == 'block') {
                for (let j of range(amount))
                    if (list[i + j]) list[i + j].classList.add('hide')
                setTimeout(() => {
                    for (let j of range(amount)) {
                        if (list[i + j]) list[i + j].style.display = 'none'
                        if (list[i + j]) list[i + j].classList.remove('hide', 'show')
                    }
                    let isLastRange = true
                    for (let j of range(amount))
                        if (list[i - amount + j]) isLastRange = false
                    if (isLastRange) {
                        let listLen = list.length
                        let array = []
                        let i = 0
                        while (i < listLen) {
                            let tmpArray = []
                            for (let j of range(amount))
                                tmpArray.push(list[i + j])
                            array.push(tmpArray)
                            i += amount
                        }
                        let len = array.length
                        for (let object of array[len - 1]) {
                            if (object) object.style.display = 'block'
                            if (object) object.classList.add('show')
                        }
                    } else for (let j of range(amount)) {
                        if (list[i - amount + j])
                            list[i - amount + j].style.display = 'block'
                        if (list[i - amount + j])
                            list[i - amount + j].classList.add('show')
                    }
                }, 310)
                break
            }
            i += 1
        }
    }
}

function getAmount() {
    let width = document.documentElement.clientWidth
    // 1199 < w <= 1399
    if (width > 1199 && width <= 1399) return 3
    // 991 < w <= 1199
    if (width > 991 && width <= 1199) return 3
    // 767 < w <= 991
    if (width > 767 && width <= 991) return 2
    // 575 < w <= 767
    if (width > 575 && width <= 767) return 1
    // w <= 575
    if (width <= 575) return 1
    // w >= 1400
    return 4
}

function initlist(list) {
    let amount = getAmount()
    for (let object of list) {
        object.classList.remove('show', 'hide')
        object.style.display = 'none'
    }
    for (let i of range(amount)) {
        list[i].style.display = 'block'
        list[i].classList.add('show')
    }
    window.amount = amount
}

let listOfSugges = document.querySelectorAll('.sugges')
let dots = document.querySelectorAll('.dot')
let listOfNews = document.querySelectorAll('.news-preview')
let newsContainer = document.querySelector('.latest-news')

for (let point of dots) point.addEventListener('click', clickDot(listOfSugges, dots))
window.addEventListener('resize', event => initlist(listOfNews))
moveLeftBtn.addEventListener('click', leftMove(listOfNews))
moveRightBtn.addEventListener('click', rightMove(listOfNews))
newsContainer.addEventListener('swiped-left', leftMove(listOfNews))
newsContainer.addEventListener('swiped-right', rightMove(listOfNews))

setValue(listOfSugges, dots, 0, '1')
initlist(listOfNews)
var timerId = setInterval(changeSuggestion, 10000, listOfSugges, dots)
