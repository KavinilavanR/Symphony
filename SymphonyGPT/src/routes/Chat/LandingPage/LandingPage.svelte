<script>
	import sunLogo from '../../../assets/svg/sun.svg';
	import zapLogo from '../../../assets/svg/zap.svg';
	import alertTriangle from '../../../assets/svg/alert-triangle.svg';

	export let questionSearch;
	export let generateResponse;
	
	const LANDING_TEMPLATE = [
		{
			// logo: sunLogo,
			// logoColorCode: '#29BBC4',
			// name: 'Examples',
			clickable: true,
			content: [
				'what is the share of brand VELCADE in last 3 months',
				'what is the average age of patient with indication MM'
			],
		},
		{
			// logo: zapLogo,
			// logoColorCode: '#36B37E',
			// name: 'Capabilities',
			clickable: true,
			content: [
				'what is the claim volume of brand VELCADE',
				'What is the growth of brand VELCADE'
			],
		}
	];
</script>

<div class="landing__header">
	<div class="landing__header-main">
		Symphony-GPT Search
	</div>
	<!-- <div class="landing__header-sub">
		I'm an early-stage prototype. Let's explore together, but be patient
		with my speed and learning curve!
	</div> -->
</div>
<div class="landing">
	{#each LANDING_TEMPLATE as template}
		<div class="landing__container">
			<!-- <div class="landing__header">
				<span
					class="landing__logo"
					style="background-color: {template.logoColorCode};"
				>
					<img src={template.logo} alt={template.name} />
				</span>
				{template.name}
			</div> -->
			{#each template.content as text}
				<button
					class="landing__text"
					class:landing__text--clickable={template.clickable}
					on:click={() => {
						if (template.clickable) {
							generateResponse(text);
						}
					}}
				>
					{text}{template.clickable ? ' →' : ''}
				</button>
			{/each}
		</div>
	{/each}
</div>

<style src="./style.scss"></style>
