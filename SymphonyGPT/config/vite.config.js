import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import path from 'path';
import { fileURLToPath } from 'url';

const filename = fileURLToPath(import.meta.url);
const projectRootDir = path.dirname(filename);

// https://vitejs.dev/config/
export default defineConfig({
	resolve: {
		alias: {
			'@components': path.resolve(
				projectRootDir,
				'../src/lib/components'
			),
			'@stores': path.resolve(projectRootDir, '../src/lib/stores'),
			'@utils': path.resolve(projectRootDir, '../src/lib/utils'),
			'@models': path.resolve(projectRootDir, '../src/lib/models'),
		},
	},
	plugins: [svelte({ configFile: './config/svelte.config.js' })],
	build: {
		target: 'es2015',
	},
	css: {
		postcss: './config/postcss.congif.js',
	},
});
