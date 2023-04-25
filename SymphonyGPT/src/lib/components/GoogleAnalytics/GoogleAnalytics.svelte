<script>
	import isEmpty from '@utils/is-empty';

	let GTM_ID = import.meta.env.VITE_GTM_ID,
		scriptSrc;

	function init() {
		if (isEmpty(GTM_ID)) {
			return;
		}

		window['dataLayer'] = window['dataLayer'] || [];
		window['dataLayer'].push({
			'gtm.start': new Date().getTime(),
			event: 'gtm.js',
		});
		scriptSrc = `https://www.googletagmanager.com/gtm.js?id=${GTM_ID}`;
	}

	init();
</script>

<svelte:head>
	{#if scriptSrc}
		<script src={scriptSrc} async></script>
	{/if}
</svelte:head>
