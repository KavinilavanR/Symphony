<script>
	import { toasts } from './toasts.js';
	import { fade, fly } from 'svelte/transition';
	import { backOut } from 'svelte/easing';
</script>

<div class="toast-wrapper">
	{#each $toasts as toast (toast._id)}
		<div
			class="toast"
			in:fly={{
				delay: 0,
				duration: 100,
				x: 0,
				y: 50,
				easing: backOut,
			}}
			out:fade={{ duration: 500 }}
		>
			<div class="toast__message">{toast.msg}</div>
		</div>
	{/each}
</div>

<style src="./style.scss">
</style>
