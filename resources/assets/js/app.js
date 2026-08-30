import { clearAlerts, showAlert, showAlerts } from './modules/alert.js';
import { getFormData } from './modules/form.js';
import { getErrorMessages, ingest } from './modules/ingest.js';
import { hideOutput, showOutput } from './modules/output.js';
import { hideLoading, showLoading } from './modules/loading.js';

const form = document.getElementById('ingest-form');

const delay = (ms) => {
	return new Promise((resolve) => setTimeout(resolve, ms));
};

const MIN_LOADING_TIME = 1000;

form.addEventListener('submit', async (event) => {
	event.preventDefault();

	clearAlerts();
	hideOutput();

	showLoading();

	const data = getFormData(form);

	try {
		const [{ response, result }] = await Promise.all([ingest(data), delay(MIN_LOADING_TIME)]);

		hideLoading();

		if (response.status !== 201) {
			showAlerts(getErrorMessages(result));

			return;
		}

		showOutput(result);
	} catch (error) {
		console.error(error);

		hideLoading();

		showAlerts(['Não foi possível conectar ao servidor.']);
	}
});
