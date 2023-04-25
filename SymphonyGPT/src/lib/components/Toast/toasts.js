import { writable } from 'svelte/store';

export const toasts = createToast();

export let pushToast = toasts.pushToast;

function createToast() {
	const { subscribe, update } = writable([]);

	let toastId = 0;

	function pushToast(msg = '', retainMs = 3000) {
		const id = ++toastId;
		update((existingToasts) => [
			...existingToasts,
			{
				_id: id,
				msg,
			},
		]);
		setTimeout(() => {
			closeToast(id);
		}, retainMs);
	}

	function closeToast(id) {
		update((existingToasts) =>
			existingToasts.filter((toast) => toast._id != id)
		);
	}

	return {
		subscribe,
		pushToast,
		closeToast,
	};
}
