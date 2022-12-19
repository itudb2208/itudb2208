function setPage(callerNode) {
	let pageNoInput = document.getElementById("pageno_input");
	let selectedPageNo = callerNode.getAttribute("value");
	pageNoInput.value = selectedPageNo;
	let setPageForm = document.getElementById("setpage_form");
	setPageForm.submit();
}