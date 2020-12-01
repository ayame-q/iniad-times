let isPreviewDiff = false;
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
		if (parentForm.dataset.is_revision_form === "true") {
			isPreviewDiff = true;
		}
		const easyMDE = new EasyMDE({
			element: textInputElement,
			autosave: {
				enabled: true,
				uniqueId: "iniad-times_" + parentForm.dataset.object_uuid,
			},
			forceSync: true,
			spellChecker: false,
			uploadImage: true,
			sideBySideFullscreen: false,
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
					uuid: parentForm.dataset.object_uuid,
				}
				const body = Object.keys(obj).map((key)=>key+"="+encodeURIComponent(obj[key])).join("&");
				let url = "/api/parse_markdown"
				if (isPreviewDiff) {
					url = "/api/get_diff"
				}
				fetch(url, {
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
			},
			toolbar: [
				"bold", "italic",
				"|",
				"heading-1", "heading-2", "heading-3",
				"|",
				"quote", "unordered-list", "ordered-list",
				"|",
				"link", "image",
				"|",
				{
					name: "preview",
					action: (editor) => {
						isPreviewDiff = false
						const toolbar = editor.gui.toolbar
						easyMDE.toggleSideBySide()
						easyMDE.toggleSideBySide()
					},
					className: "fa fa-eye",
					title: "Preview"
				},
				{
					name: "diff",
					action: (editor) => {
						isPreviewDiff = true
						const toolbar = editor.gui.toolbar
						easyMDE.toggleSideBySide()
						easyMDE.toggleSideBySide()
					},
					className: "fa fa-exchange",
					title: "Diff"
				},
				{
					name: "fullscreen",
					action: (editor) => {
						editor.toggleFullScreen()
						editor.toggleSideBySide()
					},
					className: "fa fa-arrows-alt",
					title: "FullScreen"
				},
			]
		});
		easyMDE.toggleSideBySide()
	}
});