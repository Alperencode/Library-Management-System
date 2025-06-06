const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');
const localIp = require('../local-ip.json').ip;


module.exports = defineConfig({
  productionSourceMap: false,
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
          VUE_APP_RFID_PORT: JSON.stringify(8001),
          VUE_APP_BARCODE_PORT: JSON.stringify(8001),
        },
        '__VUE_OPTIONS_API__': JSON.stringify(true),
        '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': JSON.stringify(false),
      }),
    ],
  },
});