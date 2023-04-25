<script>
	import Router from 'svelte-spa-router';
	import { routes } from './routes/routes';
	import Toast from '@components/Toast/Toast.svelte';
	import GoogleAnalytics from '@components/GoogleAnalytics/GoogleAnalytics.svelte';
</script>

<Router {routes} />
<Toast />
<GoogleAnalytics />
