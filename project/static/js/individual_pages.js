var INDIVIDUAL_PAGE_NAMES = ["tmID", "playerID", "coachID"];
var pageName = INDIVIDUAL_PAGE_NAMES.filter((name)=>location.pathname.includes(name))[0];
var modifications = {};
modifications[pageName] = document.getElementById("entryID").innerHTML;

function toggleEdit(callerNode) {
	let mode = callerNode.getAttribute("mode");
	let inputField = callerNode.previousElementSibling;
	let rowNode = callerNode.parentElement.parentElement;
	let rowIndex = rowNode.getAttribute("rowindex");
	if(mode == "normal") {
		callerNode.innerHTML = '<i class="bi bi-check-square-fill text-success"></i>';
		inputField.removeAttribute("hidden");
		callerNode.setAttribute("mode", "edit");
	} else if(mode == "edit") {
		let tableName = rowNode.getAttribute("tablename");
		if(modifications[tableName] == undefined) {
			modifications[tableName] = {}
		}
		if(modifications[tableName][rowIndex] == undefined) {
				modifications[tableName][rowIndex] = {}
		}
		modifications[tableName][rowIndex][inputField.name] = inputField.value;
		let whereKeys = rowNode.getAttribute("wherekeys");
		if(whereKeys != null) {
			modifications[tableName][rowIndex]["wherekeys"] = whereKeys;
		}
		let whereValues = rowNode.getAttribute("wherevalues");
		if(whereValues != null) {
			modifications[tableName][rowIndex]["wherevalues"] = whereValues;
		}
		callerNode.parentNode.firstElementChild.innerHTML = inputField.value;
		callerNode.innerHTML = '<i class="bi bi-pencil-square"></i>';
		inputField.setAttribute("hidden", "");
		callerNode.setAttribute("mode", "normal");
	}
}

function save() {
	fetch(`/search/${pageName}/update`, {
		method: 'POST',
		headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
		},
		body: JSON.stringify(modifications)
	});
}