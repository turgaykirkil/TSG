const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const config = getDefaultConfig(__dirname);

config.resolver.extraNodeModules = {
  ...config.resolver.extraNodeModules,
  'use-latest-callback': path.resolve(__dirname, 'src/utils/useLatestCallback.js'),
};

module.exports = config;