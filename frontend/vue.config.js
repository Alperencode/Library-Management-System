const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

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
        '__VUE_OPTIONS_API__': JSON.stringify(true),
        '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': JSON.stringify(false),
      }),
    ],
  },
});