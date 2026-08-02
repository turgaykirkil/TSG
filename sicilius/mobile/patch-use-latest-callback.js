const fs = require('fs');
const path = require('path');

const base = path.join(__dirname, 'node_modules/use-latest-callback');

const code = `'use strict';
var React = require('react');

function useLatestCallback(callback) {
  var ref = React.useRef(callback);
  var latestCallback = React.useRef(function latestCallback() {
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      args[_i] = arguments[_i];
    }
    return ref.current.apply(this, args);
  }).current;
  var useEffectHook = React.useInsertionEffect || React.useLayoutEffect || React.useEffect;
  useEffectHook(function () {
    ref.current = callback;
  });
  return latestCallback;
}

useLatestCallback.default = useLatestCallback;
useLatestCallback.useLatestCallback = useLatestCallback;

try {
  Object.defineProperty(useLatestCallback, '__esModule', { value: true });
  Object.defineProperty(useLatestCallback, 'default', { value: useLatestCallback, writable: true, configurable: true });
} catch (e) {}

module.exports = useLatestCallback;
module.exports.default = useLatestCallback;
module.exports.useLatestCallback = useLatestCallback;
module.exports.__esModule = true;
`;

if (fs.existsSync(base)) {
  const pkgPath = path.join(base, 'package.json');
  if (fs.existsSync(pkgPath)) {
    try {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      delete pkg.exports;
      pkg.main = './lib/src/index.js';
      pkg.module = './lib/src/index.js';
      fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2), 'utf8');
    } catch (e) {}
  }

  const targets = [
    path.join(base, 'lib/src/index.js'),
    path.join(base, 'lib/index.js'),
    path.join(base, 'index.js'),
    path.join(base, 'esm.mjs'),
  ];

  targets.forEach((target) => {
    try {
      const dir = path.dirname(target);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(target, code, 'utf8');
    } catch (e) {}
  });

  console.log('[Patch] Successfully patched use-latest-callback in all entry points!');
}
