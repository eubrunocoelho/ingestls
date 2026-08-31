const path = require('path');

module.exports = {
	mode: 'production',
	entry: './resources/assets/js/app.js',
	module: {
		rules: [
			{
				test: /\.js$/,
				type: 'javascript/auto',
			},
		],
	},
	output: {
		filename: 'app.min.js',
		path: path.resolve(__dirname, 'resources/assets/js/dist'),
		clean: true,
	},
	optimization: {
		minimize: true,
	},
};
