import { useRef, useInsertionEffect, useLayoutEffect, useEffect } from 'react';

function useLatestCallback<T extends (...args: any[]) => any>(callback: T): T {
  const ref = useRef(callback);
  const latestCallback = useRef(function latestCallback(this: any, ...args: any[]) {
    return ref.current.apply(this, args);
  }).current;

  const useHook = useInsertionEffect || useLayoutEffect || useEffect;
  useHook(() => {
    ref.current = callback;
  });

  return latestCallback as T;
}

(useLatestCallback as any).default = useLatestCallback;
(useLatestCallback as any).useLatestCallback = useLatestCallback;
(useLatestCallback as any).__esModule = true;

export { useLatestCallback };
export default useLatestCallback;
