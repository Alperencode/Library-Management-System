const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');
const localIp = require('../local-ip.json').ip;


module.exports = defineConfig({
  devServer: {
    port: 8085,
    client: {
      overlay: false
    }
  },
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        'process.env': {
          VUE_APP_API_HOST: JSON.stringify(localIp),
          VUE_APP_API_PORT: JSON.stringify(8000),
        },
        '__VUE_OPTIONS_API__': JSON.stringify(true),
        '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': JSON.stringify(false),
      }),
    ],
  },
});