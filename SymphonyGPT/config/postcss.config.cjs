const autoprefixer = require('autoprefixer');
const postcssPresetEnv = require('postcss-preset-env');
const postcssNormalize = require('postcss-normalize')

module.exports = {
	plugins: [
		autoprefixer(),
		postcssPresetEnv({ stage: 3 }),
		postcssNormalize({
			forceImport: 'sanitize.css'
		}),
	],
};
