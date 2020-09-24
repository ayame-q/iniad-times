window.addEventListener("load", function() {
	const textInputElements = document.getElementsByClassName("text-input");
	for(const textInputElement of textInputElements){
		const parentTextInputElement = textInputElement.parentNode;
		const textInputWrapElement = document.createElement("div");
		textInputWrapElement.classList.add("text-input-wrap");
		parentTextInputElement.appendChild(textInputWrapElement);
		textInputWrapElement.appendChild(textInputElement);
		const formElements = document.forms;
		let parentForm;
		for(const formElement of formElements){
			if(formElement.contains(textInputElement)){
				parentForm = formElement;
			}
		}
		const easyMDE = new EasyMDE({
			element: textInputElement,
			/*autosave: {
				enabled: true,
				uniqueId: "iniad-times_" + parentForm.dataset.page_id,
			},*/
			forceSync: true,
			spellChecker: false,
			uploadImage: true,
			imageMaxSize: 1024*1024*10,
			imageUploadEndpoint: "/api/upload_image",
			imageCSRFToken: Cookies.get("csrftoken"),
		});
	}
});