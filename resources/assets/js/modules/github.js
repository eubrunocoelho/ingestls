const repositoryStars = document.getElementById('repository-stars');

const STORAGE_KEY = 'repository-stars';
const CACHE_DURATION = 30 * 60 * 1000;

export async function getRepositoryStars(owner, repo) {
	const cached = localStorage.getItem(STORAGE_KEY);

	if (cached) {
		const { stars, timestamp } = JSON.parse(cached);

		if (Date.now() - timestamp < CACHE_DURATION) {
			return stars;
		}

		localStorage.removeItem(STORAGE_KEY);
	}

	const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/stargazers/count`);

	if (!response.ok) {
		throw new Error('Não foi possível obter as estrelas do repositório.');
	}

	const data = await response.json();

	localStorage.setItem(
		STORAGE_KEY,
		JSON.stringify({
			stars: data.count,
			timestamp: Date.now(),
		}),
	);

	return data.count;
}

export function showRepositoryStars(stars) {
	repositoryStars.textContent = stars;
}
