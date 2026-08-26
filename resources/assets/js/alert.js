const form = document.getElementById('ingest-form');

function getAlerts() {
	return form.parentElement.querySelector('.alerts');
}

function createAlerts() {
	let alerts = getAlerts();

	if (!alerts) {
		alerts = document.createElement('div');
		alerts.className = 'alerts';

		form.insertAdjacentElement('afterend', alerts);
	}

	return alerts;
}

export function showAlert(message, type = 'danger') {
	const alerts = createAlerts();

	const alert = document.createElement('div');

	alert.className = `alert alert--${type}`;
	alert.textContent = message;

	alerts.appendChild(alert);
}

export function clearAlerts() {
	const alerts = getAlerts();

	if (alerts) {
		alerts.remove();
	}
}
