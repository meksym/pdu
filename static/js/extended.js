"use scrict";

var mask = document.createElement("div");
let img = document.createElement("img");

img.src = "/static/image/close.svg";
img.alt = "close";

mask.className = "mask";
mask.append(img);
mask.onclick = closeList;

function closeList() {
    history.pushState(
        "",
        document.title,
        window.location.pathname + window.location.search
    );
    hashchange();
}

function hashchange(event) {
    let activeList = document.querySelector(".active-hidden-list");

    if (activeList) {
        mask.remove();

        if (!document.querySelector(".active-navigation-list"))
            document.body.style.overflow = "";

        activeList.classList.remove("active-hidden-list");
    }

    if (window.location.hash) {
        let list = document.querySelector(window.location.hash);
        if (list) {
            list.before(mask);
            document.body.style.overflow = "hidden";
            list.classList.add("active-hidden-list");
        }
    }
}

for (let span of document.querySelectorAll(".next-nested")) {
    span.onclick = (event) => {
        let list = span.nextElementSibling;

        if (list.classList.contains("active-nested"))
            list.classList.remove("active-nested");
        else
            list.classList.add("active-nested");
    };
}

for (let closeElem of document.querySelectorAll(".mobile-close-hidden-list"))
    closeElem.onclick = closeList;

openNavigation.onclick = (event) => {
    let navigation = document.querySelector(".navigation-list");
    navigation.classList.add("active-navigation-list");
    document.body.style.overflow = "hidden";
};

closeNavigation.onclick = (event) => {
    let navigation = document.querySelector(".navigation-list");
    navigation.classList.remove("active-navigation-list");
    document.body.style.overflow = "";
};

window.addEventListener("resize", (event) => {
    if (document.documentElement.clientWidth >= 767) {
        let navigation = document.querySelector(".active-navigation-list");
        if (navigation)
            navigation.classList.remove("active-navigation-list");

        if (!document.querySelector(".active-hidden-list"))
            document.body.style.overflow = "";
    }
});

window.addEventListener("hashchange", hashchange);

if (window.location.hash)
    history.pushState(
        "",
        document.title,
        window.location.pathname + window.location.search
    );
