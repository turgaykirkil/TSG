const React = require('react');

function useLatestCallback(callback) {
  const ref = React.useRef(callback);
  const latestCallback = React.useRef(function latestCallback(...args) {
    return ref.current.apply(this, args);
  }).current;

  const useHook = React.useInsertionEffect || React.useLayoutEffect || React.useEffect;
  useHook(() => {
    ref.current = callback;
  });

  return latestCallback;
}

useLatestCallback.default = useLatestCallback;
useLatestCallback.useLatestCallback = useLatestCallback;

module.exports = useLatestCallback;
module.exports.default = useLatestCallback;
module.exports.useLatestCallback = useLatestCallback;
module.exports.__esModule = true;
