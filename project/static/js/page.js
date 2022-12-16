function choicePage(page) {
    const background = document.getElementsByClassName("s002")[0];
    const title = document.getElementsByTagName("LEGEND")[0];
    switch (page) {
        case "teams":
            background.style.background = "url(../static/team.webp.png)"
            title.innerHTML = "SEARCH TEAM";
            break;
        case "players":
            background.style.background = "url(../static/player.jpg)"
            title.innerHTML = "SEARCH PLAYER";
            break;
        case "coaches":
            background.style.background = "url(../static/coach.jpg)"
            title.innerHTML = "SEARCH COACH";
            break;
        default:
            background.style.background = "url(../static/team.webp.png)"    }
}