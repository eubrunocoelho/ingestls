import { showToast } from './toast.js';

const COPIED_FEEDBACK_DURATION = 1500;

const resultSummary = document.getElementById('result-summary');
const resultStructure = document.getElementById('result-structure');
const resultFilesContent = document.getElementById('result-files-content');

const copySummary = document.getElementById('copy-summary');
const copyStructure = document.getElementById('copy-structure');
const copyFilesContent = document.getElementById('copy-files-content');
const copyAllContent = document.getElementById('copy-all-content');

async function copyText(text) {
	await navigator.clipboard.writeText(text);
}

function getAllContent() {
	return [resultSummary.textContent, resultStructure.textContent, resultFilesContent.textContent]
		.filter(Boolean)
		.join('\n\n');
}

function showCopiedFeedback(iconBox) {
	const icon = iconBox.querySelector('i');

	clearTimeout(iconBox._copiedTimeout);

	iconBox.classList.add('section-output__copy-icon-box--copied');
	icon?.classList.replace('fa-copy', 'fa-check');

	iconBox._copiedTimeout = setTimeout(() => {
		iconBox.classList.remove('section-output__copy-icon-box--copied');
		icon?.classList.replace('fa-check', 'fa-copy');
	}, COPIED_FEEDBACK_DURATION);
}

async function handleCopyClick(iconBox, text) {
	try {
		await copyText(text);

		showCopiedFeedback(iconBox);
		showToast('Copiado para a área de transferência!', 'success');
	} catch (error) {
		console.error(error);

		showToast('Não foi possível copiar o conteúdo.', 'danger');
	}
}

export function setupCopyButtons() {
	copySummary?.addEventListener('click', () => handleCopyClick(copySummary, resultSummary.textContent));

	copyStructure?.addEventListener('click', () => handleCopyClick(copyStructure, resultStructure.textContent));

	copyFilesContent?.addEventListener('click', () =>
		handleCopyClick(copyFilesContent, resultFilesContent.textContent),
	);

	copyAllContent?.addEventListener('click', () => handleCopyClick(copyAllContent, getAllContent()));
}
