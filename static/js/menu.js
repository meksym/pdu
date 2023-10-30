'use strict'


function showMenu(event) {
    document.body.style.overflow = 'hidden'
    mobileNav.className = 'show-mobile-menu'
}

function closeMenu(event) {
    document.body.style.overflow = ''
    mobileNav.className = 'hide-mobile-menu'
}

mobileNavButton.onclick = showMenu
closeMobileNav.onclick = closeMenu