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
			imageUploadFunction: (image, resolve, reject) => {
				const title = window.prompt("画像のタイトルを入力してください")
				if (!title) {
					reject("キャンセルされました。")
					return
				}
				const formData = new FormData();
				formData.append("image", image)
				formData.append("title", title)
				fetch("/api/upload_image", {
					method: "POST",
					headers: {
						"X-CSRFToken": Cookies.get("csrftoken"),
					},
					body: formData,
				})
					.then((response) => {
						return response.json()
					})
					.catch((error) => {
						reject("Error: " + error)
					})
					.then((json) => {
						if (json.error) {
							reject(json.error)
						}
						resolve(json.data.filePath)
					})
			},
			previewRender: (text) => {
				const obj = {
					text: text,
				}
				const body = Object.keys(obj).map((key)=>key+"="+encodeURIComponent(obj[key])).join("&");
				fetch("/api/parse_markdown", {
					method: "POST",
					headers: {
						'Content-Type': 'application/x-www-form-urlencoded',
						"X-CSRFToken": Cookies.get("csrftoken"),
					},
					body: body,
				})
					.then((response) => {
						return response.json()
					})
					.then((json) => {
						const previewElements = document.getElementsByClassName("editor-preview")
						for (const previewElement of previewElements) {
							previewElement.innerHTML = json.text
						}
					})
			}
		});
	}
});