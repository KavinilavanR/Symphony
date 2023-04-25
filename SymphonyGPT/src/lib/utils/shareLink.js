import { pushToast } from '@components/Toast/toasts';

export const shareLink = (link) => {
	if (navigator?.clipboard?.writeText) {
		navigator.clipboard
			.writeText(link)
			.then(() => {
				pushToast('Question copied and ready to share!');
			})
			.catch(console.error);
	} else {
		const el = document.createElement('textarea');
		el.value = link;
		el.setAttribute('readonly', '');
		el.style.position = 'absolute';
		el.style.left = '-9999px';
		document.body.appendChild(el);
		el.select();
		document.execCommand('copy');
		document.body.removeChild(el);
		pushToast('Question copied and ready to share!');
	}
};
