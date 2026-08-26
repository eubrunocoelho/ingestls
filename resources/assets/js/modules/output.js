const outputSection = document.getElementById('output');

const resultSummary = document.getElementById('result-summary');
const resultStructure = document.getElementById('result-structure');
const resultFilesContent = document.getElementById('result-files-content');

export function showOutput(output) {
	resultSummary.textContent = output.summary;
	resultStructure.textContent = output.directory_structure;
	resultFilesContent.textContent = output.files_content;

	outputSection.style.display = 'flex';
}

export function hideOutput() {
	outputSection.style.display = 'none';
}
