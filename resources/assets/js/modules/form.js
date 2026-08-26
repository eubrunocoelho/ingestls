export function getFormData(form) {
	const formData = new FormData(form);

	return {
		path: formData.get('path'),
		pattern_type: formData.get('pattern-type'),
		pattern: formData.get('pattern'),
	};
}
