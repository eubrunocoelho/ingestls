import { showToast } from './toast.js';

const resultSummary = document.getElementById('result-summary');
const resultStructure = document.getElementById('result-structure');
const resultFilesContent = document.getElementById('result-files-content');

const copySummary = document.getElementById('copy-summary');
const copyStructure = document.getElementById('copy-structure');
const copyFilesContent = document.getElementById('copy-files-content');
const copyAllContent = document.getElementById('copy-all-content');

async function copyText(text) {
	try {
		await navigator.clipboard.writeText(text);

		showToast('Copiado para a área de transferência!', 'success');
	} catch (error) {
		console.error(error);

		showToast('Não foi possível copiar o conteúdo.', 'danger');
	}
}

function getAllContent() {
	return [resultSummary.textContent, resultStructure.textContent, resultFilesContent.textContent]
		.filter(Boolean)
		.join('\n\n');
}

export function setupCopyButtons() {
	copySummary?.addEventListener('click', () => copyText(resultSummary.textContent));
	copyStructure?.addEventListener('click', () => copyText(resultStructure.textContent));
	copyFilesContent?.addEventListener('click', () => copyText(resultFilesContent.textContent));
	copyAllContent?.addEventListener('click', () => copyText(getAllContent()));
}
