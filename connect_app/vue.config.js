const webpack = require('webpack');

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        'process.env': {
          BASE_API_URL: JSON.stringify('http://127.0.0.1:8000/'),
        },
      }),
    ],
  },
};

