export async function ingest(data) {
	const response = await fetch('/ingest', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(data),
	});

	const result = await response.json();

	return {
		response,
		result,
	};
}

export function getErrorMessages(result) {
	if (result.errors?.length) {
		return result.errors.map((error) => error.message);
	}

	return [result.message ?? 'Ocorreu um erro ao processar a requisição.'];
}
