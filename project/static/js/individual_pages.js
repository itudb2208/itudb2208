var modifications = {"tmID": document.getElementById("entryID").innerHTML};
function toggleEdit(callerNode) {
	let mode = callerNode.getAttribute("mode");
	let inputField = callerNode.previousElementSibling;
	if(mode == "normal") {
		callerNode.innerHTML = '<i class="bi bi-check-square-fill text-success"></i>';
		inputField.removeAttribute("hidden");
		callerNode.setAttribute("mode", "edit");
	} else if(mode == "edit") {
		modifications[inputField.name] = inputField.value;
		callerNode.parentNode.firstElementChild.innerHTML = inputField.value;
		callerNode.innerHTML = '<i class="bi bi-pencil-square"></i>';
		inputField.setAttribute("hidden", "");
		callerNode.setAttribute("mode", "normal");
	}
}

var INDIVIDUAL_PAGE_NAMES = ["tmID", "playerID", "coachID"];
function save() {
	let pageName = INDIVIDUAL_PAGE_NAMES.filter((name)=>location.pathname.includes(name))[0];
	fetch(`/search/${pageName}/update`, {
		method: 'POST',
		headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
		},
		body: JSON.stringify(modifications)
	});
}