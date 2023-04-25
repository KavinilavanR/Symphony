<script>
	export let type = 'primary';
	export let disabled = false;
</script>

<button class="btn btn__{type}" class:disabled {disabled} on:click>
	<slot />
</button>

<style src="./style.scss">
</style>
