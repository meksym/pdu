'use strict'


function main() {
    // Customization
    window['site-name'].querySelector('a').innerText = 'Сумський Палац дітей та юнацтва'
    for (let node of window['user-tools'].childNodes) if (node.nodeType == 3) node.data = node.data.replace('/', '|')
    for (let input of document.querySelectorAll('input')) input.spellcheck = false
    for (let textarea of document.querySelectorAll('textarea')) textarea.spellcheck = false
    // Image load
    let fileInputRow = document.querySelector('.field-banner') || document.querySelector('.field-background')
    if (fileInputRow) {
        let fileInput = fileInputRow.querySelector('input[type="file"]')
        let link = fileInputRow.querySelector('a')
        let formRow = document.createElement('div')
        let banner = document.createElement('div')
        let url
        if (link) {
            link.target = '_blank'
            url = link.href
        } else url = '/static/image/main.jpg' // hard code
        banner.classList.add('view-image')
        banner.style.backgroundImage = `url(${url})`
        banner.onclick = event => fileInput.click()
        fileInput.addEventListener(
            'change',
            event => {
                let image = event.target.files[0]
                let url = URL.createObjectURL(image)
                banner.style.backgroundImage = `url('${url}')`
            }
        )
        formRow.classList.add('form-row')
        formRow.append(banner)
        fileInputRow.after(formRow)
    }
}


document.addEventListener('DOMContentLoaded', main);