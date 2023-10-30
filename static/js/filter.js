'use strict'


function countSecton() {}

function changeStateButton(event) {
    if (event.target.classList.contains('active-parameter'))
        event.target.classList.remove('active-parameter')
    else
        event.target.classList.add('active-parameter')
}

function dropFilter(event) {
    minAgeSelect.value = '1'
    maxAgeSelect.value = '18'
    for (let option of maxAgeSelect.querySelectorAll('option'))
        option.removeAttribute('disabled')
    for (let option of minAgeSelect.querySelectorAll('option'))
        option.removeAttribute('disabled')
    for (let button of filter.querySelectorAll('ul li'))
        button.classList.remove('active-parameter')
    for (let section of document.querySelectorAll('.big-section-preview'))
        section.style.display = ''
}

function restrictAge(event) {
    if (event.target == minAgeSelect) {
        let min = Number(minAgeSelect.value)
        let options = maxAgeSelect.querySelectorAll('option')
        for (let opt of options)
            opt.removeAttribute('disabled')
        for (let opt of options)
            if (Number(opt.value) < min)
                opt.setAttribute('disabled', '')
    } else if (event.target == maxAgeSelect) {
        let max = Number(maxAgeSelect.value)
        let options = minAgeSelect.querySelectorAll('option')
        for (let opt of options)
            opt.removeAttribute('disabled')
        for (let opt of options)
            if (Number(opt.value) > max)
                opt.setAttribute('disabled', '')
    } else console.error('Error')
}

function applyFilter(event) {
    let directions = []
    for (let dirElement of document.querySelectorAll('.directions li'))
        if (dirElement.classList.contains('active-parameter'))
            directions.push(dirElement.innerText)
    if (directions.length == 0)
        for (let dirElement of document.querySelectorAll('.directions li'))
            directions.push(dirElement.innerText)
    let departments = []
    for (let departElement of document.querySelectorAll('.departments li'))
        if (departElement.classList.contains('active-parameter'))
            departments.push(departElement.getAttribute('value'))
    if (departments.length == 0)
        for (let departElement of document.querySelectorAll('.departments li'))
            departments.push(departElement.getAttribute('value'))
    let minAge = Number(minAgeSelect.value)
    let maxAge = Number(maxAgeSelect.value)
    // Debug log
    console.clear()
    console.log(`VALUES OF FILTER
        AGE [${minAge}:${maxAge}]
        DIRECTIONS [${directions}]
        DEPARTMENTS [${departments}]`)
    for (let section of document.querySelectorAll('.big-section-preview')) {
        let departIntersection = false
        let ageIntersection = false
        let dirIntersection = false
        let secDirections = []
        let secMinAge = Number(section.querySelector('input[name="min_age"]').value)
        let secMaxAge = Number(section.querySelector('input[name="max_age"]').value)
        let secDepartment = section.querySelector('input[name="department"]').value
        for (let dirElement of section.querySelectorAll('input[name="direction"]'))
            secDirections.push(dirElement.value)
        // Check
        for (let i = secMinAge; i <= secMaxAge; i++)
            if (i >= minAge && i <= maxAge) {
                ageIntersection = true
                break
            }
        for (let depart of departments)
            if (depart == secDepartment)
                departIntersection = true
        for (let dir of directions)
            for (let secDir of secDirections)
                if (secDir == dir) {
                    dirIntersection = true
                    break
                }
        // View
        if (departIntersection && ageIntersection && dirIntersection)
            section.style.display = ''
        else
            section.style.display = 'none'
        // Debug log
        console.log(`${section.querySelector('.text-decoration h1').innerText}
            AGE [${secMinAge}:${secMaxAge}]
            DIRECTIONS [${secDirections}]
            DEPARTMENT ${secDepartment}
            VIEW ${departIntersection && ageIntersection && dirIntersection}`)
    }
}

dropFilterButton.addEventListener('click', dropFilter)

for (let button of filter.querySelectorAll('ul li')) {
    button.addEventListener('click', changeStateButton)
    button.addEventListener('click', applyFilter)
}

for (let select of [minAgeSelect, maxAgeSelect]) {
    select.addEventListener('change', restrictAge)
    select.addEventListener('change', applyFilter)
}

minAgeSelect.value = '1'
maxAgeSelect.value = '18'
