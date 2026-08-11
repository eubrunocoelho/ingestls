const form = document.querySelector('#ingest-form')

const outputElement = document.querySelector('#output');

const summaryElement = document.querySelector(
    '#result-summary',
);

const structureElement = document.querySelector(
    '#result-structure',
);

const fileContentElement = document.querySelector(
    '#result-file-content',
);

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const path = document.querySelector('#path').value;
    const patternType = document.querySelector('#pattern-type').value;
    const pattern = document.querySelector('#pattern').value;

    const payload = {
        path,
        pattern_type: patternType,
        pattern: pattern || null,
    };

    try {
        const response = await fetch('/ingest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            console.error(data);

            return;
        }

        structureElement.textContent = data.directory_structure ?? '';
        fileContentElement.textContent = data.files_content ?? '';

        outputElement.style.display = 'flex';
    } catch (error) {
        console.error('Erro ao realizar ingest:', error);
    }
});