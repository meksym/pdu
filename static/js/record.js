'use strict'


function onlyAllowedSymbol(string) {
    let result = true
    for (let symbol of string)
        if (symbol != '\n' && symbol != ' ') {
            result = false
            break
        }
    return result
}

if (!document.querySelector('.section-header a.dark-button'))
    for (let link of document.querySelectorAll('.section-view .inner-section p > a'))
        if (link.innerText == 'Записатися') {
            console.log(link, link.parentElement.childNodes)
            let flag = true
            for (let neighbor of link.parentElement.childNodes) {
                if (neighbor == link) continue
                if (neighbor.nodeName != '#text') {
                    flag = false
                    break
                } else if (!onlyAllowedSymbol(neighbor.data)) {
                    flag = false
                    break
                }
            }
            if (flag)
                link.classList.add('dark-button')
        }
