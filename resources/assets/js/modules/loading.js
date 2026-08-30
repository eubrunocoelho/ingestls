const inputSection = document.getElementById('input');

function getLoading() {
	return document.querySelector('.loading-wrapper');
}

function createLoading() {
	const loading = document.createElement('section');

	loading.className = 'loading-wrapper';
	loading.innerHTML = `<img src="/assets/img/loader.svg" alt="loading" />`;

	inputSection.insertAdjacentElement('afterend', loading);

	return loading;
}

export function showLoading() {
	return getLoading() ?? createLoading();
}

export function hideLoading() {
	getLoading()?.remove();
}
