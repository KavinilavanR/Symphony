import App from './App.svelte';
import './style.scss';

// import { worker } from '../mocks/server';
// if (import.meta.env.MODE === 'development') {
// 	worker.start();
// }

const app = new App({
	target: document.getElementById('app'),
});

export default app;
