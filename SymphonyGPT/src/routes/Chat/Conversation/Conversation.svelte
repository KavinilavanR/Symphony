<script>
	import { delay } from '@utils/utility';
	import { shareLink } from '@utils/shareLink';
	import zoomrxLogo from '../../../assets/svg/zoomrx-logo.svg';
	import shareIcon from '../../../assets/svg/share.svg';

	export let conversations;
	export let isSearchInprogress = false;
	export let profileColor;
	export let scrollToBottom = async () => {};

	let position = 0;
	let answerText = '';
	let splittedText = [];
	let isRendering = false;

	console.log(conversations);
	console.log(position);
	$: conversation = conversations[position];
	$: {
		isSearchInprogress = isRendering;
	}
	$: if (conversation?.response?.answer && !isRendering) {
		renderAnswer();
	}

	async function renderAnswer() {
		if (conversation.isRenderingComplete) {
			answerText = conversation?.response?.answer || '';
			return;
		}
		splittedText = conversation?.response?.answer?.split(' ') ?? [];
		if (splittedText.length) {
			isRendering = true;
			await typeWriter();
		} else {
			isRendering = false;
		}
	}
	async function typeWriter(start = 0) {
		const randomSplitValue = Math.floor(Math.random() * 7 + 5) + start;
		const textToRender = splittedText
			.slice(start, randomSplitValue)
			.join(' ');
		start = randomSplitValue;
		if (textToRender) {
			answerText = answerText + ' ' + textToRender;
			await delay(Math.floor(Math.random() * 1000 + 500));
		}
		if (start <= splittedText.length) {
			await scrollToBottom();
			await typeWriter(start);
		} else {
			await delay(Math.floor(Math.random() * 1000 + 500));
			conversation.isRenderingComplete = true;
			isRendering = false;
			await scrollToBottom();
		}
	}

	function share() {
		let url = `${window.location.origin}${window.location.pathname}#/chat?question=${encodeURIComponent(conversation.question)}`
		shareLink(url);
	}

	console.log(conversation);

</script>

<section class="conversation">
	<section class="conversation__question">
		<div class="question">
			<div class="question__profile" style="background: {profileColor};">
				<span class="question__profile-initial"> U </span>
			</div>
			<div class="question__container">
				<div class="question__container-question">
					{conversation.question}
				</div>
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div class="question__container-share" on:click={share}>
					<img src={shareIcon} alt="share" />
				</div>
			</div>
		</div>
	</section>
	<section class="conversation__response">
		<div class="conversation__response-inner">
			<div class="conversation__response-profile">
				<img src={zoomrxLogo} height = 40px alt="Ferma AI logo" />
			</div>
			<div class="conversation__response-container">
				{#if conversation.response}
					<section class="conversation__response-result">
						{@html answerText}
						{#if !conversation.isRenderingComplete}
							<span class="blinker">▋</span>
						{/if}
					</section>
					{#if conversation.response.sources?.length && conversation.isRenderingComplete}
						<hr class="response-source-separator" />
						<section class="source">
							<span class="source__title">Sources:</span>
							<ul>
								{#each conversation.response.sources as source}
									<li>
										{#if source.link}
											<a
												class="source__link"
												href={source.link}
												target="_blank"
												rel="noreferrer"
											>
												{source.title}
											</a>
										{:else}
											<span class="source__link">
												{source.title}
											</span>
										{/if}
									</li>
								{/each}
							</ul>
						</section>
					{/if}
				{:else if conversation.error}
				<div>{conversation.error}</div>
						{#if conversation.errorMessage}
							<section class="error">
								{conversation.errorMessage}
							</section>
						{:else}
							<section class="error">
								Error processing your request. Please try again later.
							</section>
						{/if}
				{:else}
					<span class="blinker blinker--initial">▋</span>
				{/if}
			</div>
		</div>
	</section>
</section>

<style src="./style.scss"></style>
