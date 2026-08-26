import { clearAlerts, showAlerts } from './modules/alert.js';
import { getFormData } from './modules/form.js';
import { getErrorMessages, ingest } from './modules/ingest.js';
import { hideOutput, showOutput } from './modules/output.js';


const form = document.getElementById('ingest-form');

let output = null;

form.addEventListener('submit', async (event) => {
	event.preventDefault();

	clearAlerts();

	const data = getFormData(form);

	try {
		const { response, result } = await ingest(data);

		if (response.status !== 201) {
			showAlerts(getErrorMessages(result));

			return;
		}

		output = result;

		showOutput(output);
	} catch (error) {
		console.error(error);

		showAlerts(['Não foi possível conectar ao servidor.']);
	}
});
