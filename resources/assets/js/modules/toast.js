const TOAST_DURATION = 4000;
const TOAST_TRANSITION_DURATION = 300;

function getToastContainer() {
	return document.getElementById('toast-container');
}

function createToastContainer() {
	const container = document.createElement('div');

	container.className = 'toast-container';
	container.id = 'toast-container';
	container.setAttribute('aria-live', 'polite');
	container.setAttribute('aria-atomic', 'true');

	document.body.appendChild(container);

	return container;
}

function getOrCreateToastContainer() {
	return getToastContainer() ?? createToastContainer();
}

function removeToast(toast) {
	toast.classList.remove('toast--visible');
	toast.classList.add('toast--hiding');

	toast.addEventListener(
		'transitionend',
		() => {
			toast.remove();
		},
		{
			once: true,
		},
	);
}

export function showToast(message, type = 'success') {
	const container = getOrCreateToastContainer();

	const toast = document.createElement('div');

	toast.className = `toast toast--${type}`;

	const toastMessage = document.createElement('p');

	toastMessage.className = 'toast__message';
	toastMessage.textContent = message;

	toast.appendChild(toastMessage);
	container.appendChild(toast);

	requestAnimationFrame(() => {
		toast.classList.add('toast--visible');
	});

	setTimeout(() => {
		removeToast(toast);
	}, TOAST_DURATION);
}
