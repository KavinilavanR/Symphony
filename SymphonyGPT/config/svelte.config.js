import { defineConfig } from 'vite';
import sveltePreprocess from 'svelte-preprocess';

export default defineConfig({
	preprocess: sveltePreprocess(),
});
