const form = document.getElementById('ingest-form');

function getAlerts() {
	return form.parentElement.querySelector('.alerts');
}

function createAlerts() {
	const alerts = document.createElement('div');

	alerts.className = 'alerts';

	form.insertAdjacentElement('afterend', alerts);

	return alerts;
}

function getOrCreatAlerts() {
	return getAlerts() ?? createAlerts();
}

export function showAlert(message, type = 'danger') {
	const alerts = getOrCreatAlerts();

	const alert = document.createElement('div');

	alert.className = `alert alert--${type}`;
	alert.textContent = message;

	alerts.appendChild(alert);
}

export function showAlerts(messages, type = 'danger') {
	messages.forEach((message) => showAlert(message, type));
}

export function clearAlerts() {
	getAlerts()?.remove();
}
