import { clearAlerts, showAlerts } from './modules/alert.js';
import { getFormData } from './modules/form.js';
import { getErrorMessages, ingest } from './modules/ingest.js';
import { hideOutput, showOutput } from './modules/output.js';
import { hideLoading, showLoading } from './modules/loading.js';
import { showToast } from './modules/toast.js';
import { setupCopyButtons } from './modules/copy.js';
import { getRepositoryStars, showRepositoryStars } from './modules/github.js';

getRepositoryStars('eubrunocoelho', 'ingestls').then(showRepositoryStars).catch(console.error);

const form = document.getElementById('ingest-form');

const delay = (ms) => {
	return new Promise((resolve) => setTimeout(resolve, ms));
};

const MIN_LOADING_TIME = 1000;

setupCopyButtons();

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
			showToast('Ocorreu um erro ao processar a requisição.', 'danger');

			return;
		}

		showOutput(result);
		showToast('Requisição processada com sucesso!', 'success');
	} catch (error) {
		console.error(error);

		hideLoading();

		showAlerts(['Não foi possível conectar ao servidor.']);
		showToast('Não foi possível conectar ao servidor.', 'danger');
	}
});
