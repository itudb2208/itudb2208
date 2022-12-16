var hiddenInput = document.getElementById("search_mode_input");
hiddenInput.value = "Teams";

function choicePage(page) {
    const background = document.getElementsByClassName("s002")[0];
    const title = document.getElementsByTagName("LEGEND")[0];
    switch (page) {
        case "team":
            background.style.background = "url(../static/team.webp.png)"
            title.innerHTML = "SEARCH TEAM";
			hiddenInput.value = "Teams";
            break;
        case "player":
            background.style.background = "url(../static/player.jpg)"
            title.innerHTML = "SEARCH PLAYER";
			hiddenInput.value = "Master";
            break;
        case "coach":
            background.style.background = "url(../static/search_img.png)"
            title.innerHTML = "SEARCH COACH";
			hiddenInput.value = "Master";
            break;
        default:
            background.style.background = "url(../static/team.webp.png)"
	}
}