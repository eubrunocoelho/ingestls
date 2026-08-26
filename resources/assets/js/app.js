import { clearAlerts, showAlert } from './alert.js';

const form = document.getElementById('ingest-form');

form.addEventListener('submit', async (event) => {
	event.preventDefault();

	clearAlerts();

	const formData = new FormData(form);

	const data = {
		path: formData.get('path'),
		pattern_type: formData.get('pattern-type'),
		pattern: formData.get('pattern'),
	};

	try {
		const response = await fetch('/ingest', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		});

		const result = await response.json();

		if (response.status !== 201) {
			if (result.errors?.length) {
				result.errors.forEach((error) => {
					showAlert(error.message);
				});
			} else {
				showAlert(result.message ?? 'Ocorreu um erro ao processar a requisição.');
			}

			return;
		}

		clearAlerts();

		console.log(result);
	} catch (error) {
		console.error(error);

		showAlert('Não foi possível conectar ao servidor.');
	}
});
