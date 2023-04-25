<script>
	import { get } from '@utils/api';
	import SearchBar from '@components/SearchBar/SearchBar.svelte';
	import Conversation from './Conversation/Conversation.svelte';
	import Button from '@components/Button/Button.svelte';
	import { onMount, onDestroy, tick } from 'svelte';
	import { v4 as uuidv4 } from 'uuid';
	import pptxgen from 'pptxgenjs';
	import { querystring } from 'svelte-spa-router';
	import fermaFullLogo from '../../assets/svg/ferma-full-logo.svg';
	import chatGPTLogo from '../../assets/svg/chatGPT.svg';
	import arrowDown from '../../assets/svg/arrow-down.svg';
	import LandingPage from './LandingPage/LandingPage.svelte';
	import ChatSideBar from './ChatSideBar/ChatSideBar.svelte';
	import hamburgerIcon from '../../assets/svg/hamburger.svg';
	import fileText from '../../assets/svg/file-text.svg';
	import fermaLogo from '../../assets/svg/ferma-logo.svg';
	import zoomrxlogo from '../../assets/svg/zoomrx-logo.svg'
	import megaPhone from '../../assets/svg/mega-phone.svg';
	import crossIcon from '../../assets/svg/cross.svg';
	import pfizer from '../../assets/svg/pfizer.svg';
	import bistol from '../../assets/svg/bistol.svg';
	import gsk from '../../assets/svg/gsk.svg';
	import janssen from '../../assets/svg/janssen.svg';
	import { configure, getLogger } from 'log4js';
	import path from 'path';
	import {
		CUSTOM_QUESTIONS,
		EXPORT_TABLE_AS_PPT_QUESTION,
		EXPORT_ABSTRACTS_AS_CSV,
		EXPORT_ABSTRACTS_AS_CSV_TWO,
	} from '@utils/constants';

	let questionSearch = '';
	let conversations = [];
	let isSearchInprogress = false;
	let showScrollToBottom = true;
	const profileConversationColor =
		'hsl(' + Math.random() * 360 + ', 100%, 30%)';
	const mediaQuery = window.matchMedia('(min-width: 768px)');
	let chatContainer, footerContainer;
	let previousScroll = 0;
	let hideScrollBtnTimer;
	let isMobileView = false;
	$: showSideBar = !isMobileView;

	function handleQueryParams() {
		let question = new URLSearchParams($querystring).get('question');
		question?.trim() && generateResponse(question);
	}

	onMount(async () => {
		handleQueryParams();
		chatContainer.style.marginBottom = `${footerContainer.clientHeight}px`;
		await scrollChatContainerToBottom();
		handleTabletChange(mediaQuery);
		chatContainer.addEventListener('scroll', toggleShowScrollToBottom);
		mediaQuery.addEventListener('change', handleTabletChange);
	});
	onDestroy(() => {
		chatContainer.removeEventListener('scroll', toggleShowScrollToBottom);
		mediaQuery.removeEventListener('change', handleTabletChange);
	});
	function handleTabletChange(e) {
		isMobileView = !e.matches;
	}
	function toggleShowScrollToBottom() {
		showScrollToBottom = chatContainer.scrollTop > previousScroll;
		previousScroll = chatContainer.scrollTop;
		if (showScrollToBottom) {
			clearTimeout(hideScrollBtnTimer);
			hideScrollBtnTimer = setTimeout(() => {
				showScrollToBottom = false;
			}, 5000);
		}
	}
	async function scrollChatContainerToBottom() {
		await tick();
		chatContainer.scrollTop = chatContainer.scrollHeight;
	}
	function convertListToHTML(answer) {
		let content =
			`The top ${answer.length} results are:` +
			'<ol>' +
			answer.reduce((accumulator, record) => {
				if (record?.abstract_link) {
					return (
						accumulator +
						`<li><a href=${
							record.abstract_link
						} target="_blank" rel="noreferrer">${(
							(record?.abstract_id || '') +
							' ' +
							(record?.title || '')
						).trim()}</a></li>`
					);
				}
				return (
					accumulator +
					`<li>${(
						(record?.abstract_id || '') +
						' ' +
						(record?.title || '')
					).trim()}</li>`
				);
			}, '') +
			'</ol>';
		return content;
	}
	function concatAnswer(answer) {
		return answer.reduce((acc, record) => {
			return acc + record + '\n';
		}, '');
	}
	async function getResponseFromServer(question, index) {
		let { responseData } = await get('/index.php', {
			question,
		});
		// let logFilePath = path.join(__dirname, 'logs', 'debug.log');
		// console.log("path",logFilePath);
		// Configure log4js
		// configure({
		// 	appenders: {
		// 		debug: {
		// 			type: 'file',
		// 			filename: logFilePath,
		// 			// ... other options ...
		// 		},
		// 	},
		// 	categories: {
		// 		default: {
		// 			appenders: ['debug'],
		// 			level: 'debug',
		// 		},
		// 	},
		// });

		// // Get logger
		// const logger = getLogger('debug');
		// logger.debug("hello");
		console.log(responseData);
		// console.log('hello',responseData.responseData);
		const tableIds = [];
		if (Array.isArray(responseData.answer)) {
			if (!responseData.answer.length) {
				responseData.answer = 'No results found';
			} else {
				let answer = responseData.answer;
				// convert to string
				responseData.answer = concatAnswer(answer);
				// CSV format
				responseData.csv = [Object.keys(answer[0]).join(',')]
					.concat(
						answer.map((record) =>
							Object.values(record)
								.map((str) => `"${str}"`)
								.join(',')
						)
					)
					.join('\n');
			}
		} else {
			responseData.answer = responseData.answer.replaceAll(
				/<table>/g,
				function () {
					const tableId = `table-${uuidv4()}`;
					tableIds.push(tableId);
					return `<table id="${tableId}">`;
				}
			);
		}
		if (tableIds.length) {
			conversations[index][conversations[index].length - 1].tableIds =
				tableIds;
		}
		conversations[index][conversations[index].length - 1].response =
			responseData;

		// Skip typwriter effect
		// VP: why type writer effect is skipped here
		if (responseData.csv) {
			conversations[index][
				conversations[index].length - 1
			].isRenderingComplete = false;
			isSearchInprogress = false;
		}
		console.log('conversation', conversations);
	}
	async function getCustomResponse(question, index) {
		if (question.toLowerCase().trim() === EXPORT_TABLE_AS_PPT_QUESTION) {
			await exportHtmlTableAsPPT(index);
		}
		if (
			question.toLowerCase().trim() === EXPORT_ABSTRACTS_AS_CSV ||
			question.toLowerCase().trim() === EXPORT_ABSTRACTS_AS_CSV_TWO
		) {
			await exportHtmlContentAsCSV(index);
		}
	}

	async function exportHtmlContentAsCSV(index) {
		if (index == 0) {
			conversations[0][0].response = {
				answer: 'No previous response found.',
			};
			return;
		}
		const lastConversation =
			conversations[index - 1][conversations[index - 1].length - 1];
		if (!lastConversation?.response?.csv || index < 1) {
			conversations[index][conversations[index].length - 1].response = {
				answer: 'No abstracts found in the previous response.',
			};
			return;
		}
		let blob = new Blob([lastConversation.response.csv], {
			type: 'text/csv',
		});
		let url = URL.createObjectURL(blob);
		let link = document.createElement('a');
		link.setAttribute('href', url);
		link.setAttribute('download', 'Abstracts.csv');
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);

		conversations[index][conversations[index].length - 1].response = {
			answer: 'Abstracts along with comprehensive details have been successfully downloaded',
		};
	}

	async function exportHtmlTableAsPPT(index) {
		if (index == 0) {
			conversations[0][0].response = {
				answer: 'No previous response found.',
			};
			return;
		}
		const lastConversation =
			conversations[index - 1][conversations[index - 1].length - 1];
		if (!lastConversation.tableIds || index < 1) {
			conversations[index][conversations[index].length - 1].response = {
				answer: 'No tables found in the previous response.',
			};
			return;
		}
		let pptx = new pptxgen();
		lastConversation.tableIds.forEach((tableId) => {
			pptx.tableToSlides(tableId);
		});
		await pptx.writeFile({ fileName: 'presentation.pptx' });
		conversations[index][conversations[index].length - 1].response = {
			answer: 'Previous response tables are downloaded as PPT.',
		};
	}
	async function generateResponse(question, index = conversations.length) {
		questionSearch = '';
		if (question === '') {
			return;
		}
		/**
		 * if default index then its a new response
		 * else its a re-generated response for same question then
		 * remaining conversations are removed
		 */
		if (index === conversations.length) {
			conversations.push([{ question }]);
		}
		conversations = conversations.slice(0, index + 1);
		await scrollChatContainerToBottom();
		isSearchInprogress = true;
		try {
			if (CUSTOM_QUESTIONS.includes(question.toLowerCase().trim())) {
				await getCustomResponse(question, index);
			} else {
				await getResponseFromServer(question, index);
			}
		} catch (error) {
			conversations[index][conversations[index].length - 1].error = true;
			if (error === 504) {
				conversations[index][
					conversations[index].length - 1
				].errorMessage = 'Request Timed Out. Please try again later.';
			}
			isSearchInprogress = false;
		} finally {
			conversations = conversations;
			await scrollChatContainerToBottom();
		}
	}
	function redirectToDemo() {
		// window.open(
		// 	'https://meetings.salesloft.com/zoomrx/vivekanandanmathivanan',
		// 	'_blank'
		// );
	}

	function reload() {
		window.location.href = `${window.location.origin}${window.location.pathname}#/chat`;
		window.location.reload();
	}

	function redirectTo(url) {
		window.open(url, '_blank');
	}
</script>

<main class="chat">
	<header class="chat__header">
		{#if isMobileView}
			{#if showSideBar}
				<button
					class="chat__header-sidebar-icon"
					on:click={() => {
						showSideBar = false;
					}}
				>
					<img src={crossIcon} alt="close sidebar" />
				</button>
			{:else}
				<button
					class="chat__header-sidebar-icon"
					on:click={() => {
						showSideBar = true;
					}}
				>
					<img src={hamburgerIcon} alt="open sidebar" />
				</button>
			{/if}
		{/if}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- <img
			class="chat__header-logo"
			src={fermaFullLogo}
			alt="Ferma logo"
			on:click={reload}
		/> -->
		<div class="chat__header-logo" on:click={reload}>
			<img src={zoomrxlogo} height = 40px alt="Ferma AI logo" />
			<span> Symphony-GPT </span>
		</div>
	</header>
	<section class="chat__outer">
		<!-- {#if isMobileView}
			<ChatSideBar bind:showSideBar {isMobileView} />
		{/if} -->
		<section class="chat__inner">
			<section class="chat__container" bind:this={chatContainer}>
				{#if conversations.length === 0}
					<LandingPage bind:questionSearch {generateResponse} />
				{:else}
					{#each conversations as conversation, i (conversation)}
						<Conversation
							bind:isSearchInprogress
							profileColor={profileConversationColor}
							conversations={conversation}
							scrollToBottom={scrollChatContainerToBottom}
						/>
					{/each}
				{/if}
			</section>
			<footer class="chat__footer" bind:this={footerContainer}>
				<section class="chat__search-bar">
					{#if conversations.length > 1 && showScrollToBottom}
						<button
							class="scroll-to-bottom"
							on:click={scrollChatContainerToBottom}
						>
							<img src={arrowDown} alt="scroll to bottom" />
						</button>
					{/if}
					<SearchBar
						focusOnLoad={true}
						bind:value={questionSearch}
						disableSearchBtn={isSearchInprogress}
						onClickHandler={() => generateResponse(questionSearch)}
					/>
				</section>
				<!-- <div class="chat__footer-info">
					<hr class="chat__footer-divider" />
					<div class="chat__footer-shedule-demo">
						<div class="chat__footer-shedule-demo-content">
							Revolutionize pharma conference coverage for Medical
							Affairs, Competitive Intelligence, and BD teams with
							Ferma.AI
						</div>
						<div class="chat__footer-shedule-demo-action">
							<Button on:click={redirectToDemo}>
								SCHEDULE A DEMO
							</Button>
						</div>
					</div>
				</div> -->
			</footer>
		</section>
	</section>
</main>

<style src="./style.scss"></style>
