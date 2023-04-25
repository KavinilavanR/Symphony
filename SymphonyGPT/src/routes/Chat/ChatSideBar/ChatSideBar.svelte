<script>
	import SideBar from '@components/SideBar/SideBar.svelte';
	import fileText from '../../../assets/svg/file-text-black.svg';
	import zoomrxLogo from '../../../assets/svg/zoomrx-logo.svg';
	import megaPhone from '../../../assets/svg/mega-phone.svg';

	export let showSideBar = true;
	export let isMobileView = false;

	const bottomSideBarMenu = [
		{
			icon: fileText,
			text: 'Whitepaper',
			disabled: false,
			onClick: () => {
				window.open('https://zoomrx.com/reports/ferma-chatgpt-revolutionizing-pharma/Revolutionizing_Pharma_The_Power_of_Large_Language_Models_and_ChatGPT.pdf', '_blank');
			},
		},
		{
			icon: megaPhone,
			text: 'Newsletter',
			disabled: false,
			onClick: () => {
				window.open('https://www.linkedin.com/newsletters/ferma-ai-chatgpt-7028308269257424896/', '_blank');
			},
		},
		{
			icon: fermaLogo,
			text: 'About',
			disabled: false,
			onClick: () => {
				window.open('https://www.ferma.ai/', '_blank');
			},
		}
	];
</script>

<SideBar
	show={showSideBar}
	position="left"
	isStatic={!isMobileView}
	toggle={() => {
		showSideBar = false;
	}}
>
	<aside class="sidebar">
		<section class="sidebar__container sidebar__container--top" />
		<section class="sidebar__container sidebar__container--bottom">
			{#each bottomSideBarMenu as menu}
				<button
					class="sidebar__menu"
					on:click={() => {
						menu.onClick && menu.onClick();
					}}
				>
					<img src={menu.icon} alt={menu.text} />
					{menu.text}
				</button>
			{/each}
		</section>
	</aside>
</SideBar>

<style src="./style.scss"></style>
