import isEmpty from '@utils/is-empty.js';

export const get = async (url = '', params = {}, headers = {}) => {
	if (!isEmpty(params)) {
		url = url + '?' + new URLSearchParams(params).toString();
	}

	const response = await fetch(import.meta.env.VITE_API_URL + url, {
		headers: {
			'Content-Type': 'application/json',
			
			...headers,
		},
	});

	return await responseHandler(response);
};

async function responseHandler(response) {
	const isJson = response.headers
		.get('content-type')
		?.includes('application/json');
	let responseData = isJson ? await response.json() : null;

	if (!response.ok) {
		const error = (responseData && responseData.message) || response.status;
		return Promise.reject(error);
	}

	return Promise.resolve({ responseData, response });
}
