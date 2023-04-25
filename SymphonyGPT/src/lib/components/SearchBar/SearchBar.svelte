<script>
	import { onDestroy, onMount, tick } from 'svelte';
	import sendIcon from '../../../assets/svg/send.svg';

	export let value = '';
	export let placeholder = 'Ask me anything...';
	export let disableSearchBtn = false;
	export let onClickHandler = () => {};
	export let focusOnLoad = false;

	let searchBarElement;

	onMount(() => {
		if (focusOnLoad) {
			searchBarElement.focus();
		}
		searchBarElement.addEventListener('paste', onPasteHandler);
	});
	onDestroy(() => {
		searchBarElement.removeEventListener('paste', onPasteHandler);
	});

	async function onPasteHandler(e) {
		e.preventDefault();
		value = value + e.clipboardData.getData('text/plain');

		await tick();
		let selection = document.getSelection();
		let range = document.createRange();
		range.setStart(
			searchBarElement.childNodes[0],
			searchBarElement.innerText.length
		);
		range.collapse(true);
		selection.removeAllRanges();
		selection.addRange(range);
	}
</script>

<section class="search-bar">
	<span
		bind:this={searchBarElement}
		role="textbox"
		contenteditable="true"
		data-ph={placeholder}
		class="search-bar__text"
		bind:textContent={value}
		on:keydown={(e) => {
			if (e.code === 'Enter' && !e.shiftKey) {
				e.preventDefault();
				!disableSearchBtn && onClickHandler();
			} else if (e.code === 'Enter' && e.shiftKey) {
				searchBarElement.value = searchBarElement.value + '\n';
				return false;
			}
		}}
	/>
	<button
		class="search-bar__send"
		on:click={onClickHandler}
		disabled={disableSearchBtn}
	>
		{#if !disableSearchBtn}
			<img class="search-bar__send-img" src={sendIcon} alt="search" />
		{:else}
			<div class="loading">
				<div class="loading__dot-typing" />
			</div>
		{/if}
	</button>
</section>

<style src="./style.scss"></style>
