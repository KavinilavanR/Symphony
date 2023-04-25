<script>
	import { fade, fly } from 'svelte/transition';

	export let show = false;
	export let position = 'left';
	export let toggle;
	export let isStatic = true;
	const transitionOffset = {
		left: {
			axis: 'x',
			offset: -1000,
		},
		right: {
			axis: 'x',
			offset: 1000,
		},
		top: {
			axis: 'y',
			offset: -1000,
		},
		bottom: {
			axis: 'y',
			offset: 1000,
		},
	};
</script>

{#if isStatic}
	<aside class="sidebar sidebar--{position} sidebar--static">
		<slot />
	</aside>
{:else if show}
	<aside
		class="sidebar sidebar--{position}"
		transition:fly={{
			[transitionOffset[position].axis]:
				transitionOffset[position].offset,
		}}
	>
		<slot />
	</aside>
	<button class="overlay" transition:fade on:click={toggle} />
{/if}

<!--
    Usage:

    let show = false;
	let position = 'right';

	const toggle = () => {
		show = !show;
	};

    <SideBar {show} {position} {toggle}>
        ...
    </SideBar>

-->
<style src="./style.scss">
</style>
