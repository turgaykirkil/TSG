[2026-03-26 19:46:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:46:13] [FRONTEND]       address: '::1',
[2026-03-26 19:46:13] [FRONTEND]       port: 5001
[2026-03-26 19:46:13] [FRONTEND]     },
[2026-03-26 19:46:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:46:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:46:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:46:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:46:13] [FRONTEND]       errno: -61,
[2026-03-26 19:46:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:46:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:46:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:46:13] [FRONTEND]       port: 5001
[2026-03-26 19:46:13] [FRONTEND]     }
[2026-03-26 19:46:13] [FRONTEND]   ]
[2026-03-26 19:46:13] [FRONTEND] }
[2026-03-26 19:46:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:46:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:46:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:46:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:46:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:46:13] [FRONTEND]   [errors]: [
[2026-03-26 19:46:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:46:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:46:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:46:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:46:13] [FRONTEND]       errno: -61,
[2026-03-26 19:46:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:46:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:46:13] [FRONTEND]       address: '::1',
[2026-03-26 19:46:13] [FRONTEND]       port: 5001
[2026-03-26 19:46:13] [FRONTEND]     },
[2026-03-26 19:46:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:46:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:46:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:46:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:46:13] [FRONTEND]       errno: -61,
[2026-03-26 19:46:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:46:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:46:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:46:13] [FRONTEND]       port: 5001
[2026-03-26 19:46:13] [FRONTEND]     }
[2026-03-26 19:46:13] [FRONTEND]   ]
[2026-03-26 19:46:13] [FRONTEND] }
[2026-03-26 19:47:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:47:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:47:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:47:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:47:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:47:13] [FRONTEND]   [errors]: [
[2026-03-26 19:47:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:47:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:47:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:47:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:47:13] [FRONTEND]       errno: -61,
[2026-03-26 19:47:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:47:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:47:13] [FRONTEND]       address: '::1',
[2026-03-26 19:47:13] [FRONTEND]       port: 5001
[2026-03-26 19:47:13] [FRONTEND]     },
[2026-03-26 19:47:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:47:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:47:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:47:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:47:13] [FRONTEND]       errno: -61,
[2026-03-26 19:47:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:47:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:47:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:47:13] [FRONTEND]       port: 5001
[2026-03-26 19:47:13] [FRONTEND]     }
[2026-03-26 19:47:13] [FRONTEND]   ]
[2026-03-26 19:47:13] [FRONTEND] }
[2026-03-26 19:47:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:47:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:47:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:47:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:47:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:47:13] [FRONTEND]   [errors]: [
[2026-03-26 19:47:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:47:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:47:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:47:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:47:13] [FRONTEND]       errno: -61,
[2026-03-26 19:47:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:47:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:47:13] [FRONTEND]       address: '::1',
[2026-03-26 19:47:13] [FRONTEND]       port: 5001
[2026-03-26 19:47:13] [FRONTEND]     },
[2026-03-26 19:47:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:47:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:47:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:47:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:47:13] [FRONTEND]       errno: -61,
[2026-03-26 19:47:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:47:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:47:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:47:13] [FRONTEND]       port: 5001
[2026-03-26 19:47:13] [FRONTEND]     }
[2026-03-26 19:47:13] [FRONTEND]   ]
[2026-03-26 19:47:13] [FRONTEND] }
[2026-03-26 19:48:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:48:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:48:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:48:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:48:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:48:13] [FRONTEND]   [errors]: [
[2026-03-26 19:48:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:48:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:48:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:48:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:48:13] [FRONTEND]       errno: -61,
[2026-03-26 19:48:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:48:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:48:13] [FRONTEND]       address: '::1',
[2026-03-26 19:48:13] [FRONTEND]       port: 5001
[2026-03-26 19:48:13] [FRONTEND]     },
[2026-03-26 19:48:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:48:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:48:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:48:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:48:13] [FRONTEND]       errno: -61,
[2026-03-26 19:48:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:48:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:48:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:48:13] [FRONTEND]       port: 5001
[2026-03-26 19:48:13] [FRONTEND]     }
[2026-03-26 19:48:13] [FRONTEND]   ]
[2026-03-26 19:48:13] [FRONTEND] }
[2026-03-26 19:48:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:48:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:48:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:48:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:48:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:48:13] [FRONTEND]   [errors]: [
[2026-03-26 19:48:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:48:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:48:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:48:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:48:13] [FRONTEND]       errno: -61,
[2026-03-26 19:48:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:48:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:48:13] [FRONTEND]       address: '::1',
[2026-03-26 19:48:13] [FRONTEND]       port: 5001
[2026-03-26 19:48:13] [FRONTEND]     },
[2026-03-26 19:48:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:48:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:48:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:48:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:48:13] [FRONTEND]       errno: -61,
[2026-03-26 19:48:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:48:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:48:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:48:13] [FRONTEND]       port: 5001
[2026-03-26 19:48:13] [FRONTEND]     }
[2026-03-26 19:48:13] [FRONTEND]   ]
[2026-03-26 19:48:13] [FRONTEND] }
[2026-03-26 19:49:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:49:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:49:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:49:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:49:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:49:13] [FRONTEND]   [errors]: [
[2026-03-26 19:49:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:49:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:49:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:49:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:49:13] [FRONTEND]       errno: -61,
[2026-03-26 19:49:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:49:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:49:13] [FRONTEND]       address: '::1',
[2026-03-26 19:49:13] [FRONTEND]       port: 5001
[2026-03-26 19:49:13] [FRONTEND]     },
[2026-03-26 19:49:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:49:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:49:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:49:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:49:13] [FRONTEND]       errno: -61,
[2026-03-26 19:49:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:49:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:49:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:49:13] [FRONTEND]       port: 5001
[2026-03-26 19:49:13] [FRONTEND]     }
[2026-03-26 19:49:13] [FRONTEND]   ]
[2026-03-26 19:49:13] [FRONTEND] }
[2026-03-26 19:49:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:49:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:49:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:49:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:49:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:49:13] [FRONTEND]   [errors]: [
[2026-03-26 19:49:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:49:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:49:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:49:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:49:13] [FRONTEND]       errno: -61,
[2026-03-26 19:49:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:49:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:49:13] [FRONTEND]       address: '::1',
[2026-03-26 19:49:13] [FRONTEND]       port: 5001
[2026-03-26 19:49:13] [FRONTEND]     },
[2026-03-26 19:49:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:49:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:49:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:49:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:49:13] [FRONTEND]       errno: -61,
[2026-03-26 19:49:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:49:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:49:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:49:13] [FRONTEND]       port: 5001
[2026-03-26 19:49:13] [FRONTEND]     }
[2026-03-26 19:49:13] [FRONTEND]   ]
[2026-03-26 19:49:13] [FRONTEND] }
[2026-03-26 19:50:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:50:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:50:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:50:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:50:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:50:13] [FRONTEND]   [errors]: [
[2026-03-26 19:50:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:50:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:50:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:50:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:50:13] [FRONTEND]       errno: -61,
[2026-03-26 19:50:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:50:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:50:13] [FRONTEND]       address: '::1',
[2026-03-26 19:50:13] [FRONTEND]       port: 5001
[2026-03-26 19:50:13] [FRONTEND]     },
[2026-03-26 19:50:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:50:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:50:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:50:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:50:13] [FRONTEND]       errno: -61,
[2026-03-26 19:50:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:50:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:50:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:50:13] [FRONTEND]       port: 5001
[2026-03-26 19:50:13] [FRONTEND]     }
[2026-03-26 19:50:13] [FRONTEND]   ]
[2026-03-26 19:50:13] [FRONTEND] }
[2026-03-26 19:50:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:50:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:50:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:50:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:50:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:50:13] [FRONTEND]   [errors]: [
[2026-03-26 19:50:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:50:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:50:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:50:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:50:13] [FRONTEND]       errno: -61,
[2026-03-26 19:50:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:50:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:50:13] [FRONTEND]       address: '::1',
[2026-03-26 19:50:13] [FRONTEND]       port: 5001
[2026-03-26 19:50:13] [FRONTEND]     },
[2026-03-26 19:50:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:50:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:50:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:50:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:50:13] [FRONTEND]       errno: -61,
[2026-03-26 19:50:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:50:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:50:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:50:13] [FRONTEND]       port: 5001
[2026-03-26 19:50:13] [FRONTEND]     }
[2026-03-26 19:50:13] [FRONTEND]   ]
[2026-03-26 19:50:13] [FRONTEND] }
[2026-03-26 19:51:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:51:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:51:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:51:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:51:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:51:13] [FRONTEND]   [errors]: [
[2026-03-26 19:51:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:51:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:51:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:51:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:51:13] [FRONTEND]       errno: -61,
[2026-03-26 19:51:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:51:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:51:13] [FRONTEND]       address: '::1',
[2026-03-26 19:51:13] [FRONTEND]       port: 5001
[2026-03-26 19:51:13] [FRONTEND]     },
[2026-03-26 19:51:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:51:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:51:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:51:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:51:13] [FRONTEND]       errno: -61,
[2026-03-26 19:51:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:51:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:51:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:51:13] [FRONTEND]       port: 5001
[2026-03-26 19:51:13] [FRONTEND]     }
[2026-03-26 19:51:13] [FRONTEND]   ]
[2026-03-26 19:51:13] [FRONTEND] }
[2026-03-26 19:51:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:51:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:51:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:51:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:51:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:51:13] [FRONTEND]   [errors]: [
[2026-03-26 19:51:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:51:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:51:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:51:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:51:13] [FRONTEND]       errno: -61,
[2026-03-26 19:51:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:51:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:51:13] [FRONTEND]       address: '::1',
[2026-03-26 19:51:13] [FRONTEND]       port: 5001
[2026-03-26 19:51:13] [FRONTEND]     },
[2026-03-26 19:51:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:51:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:51:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:51:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:51:13] [FRONTEND]       errno: -61,
[2026-03-26 19:51:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:51:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:51:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:51:13] [FRONTEND]       port: 5001
[2026-03-26 19:51:13] [FRONTEND]     }
[2026-03-26 19:51:13] [FRONTEND]   ]
[2026-03-26 19:51:13] [FRONTEND] }
[2026-03-26 19:52:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:52:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:52:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:52:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:52:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:52:13] [FRONTEND]   [errors]: [
[2026-03-26 19:52:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:52:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:52:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:52:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:52:13] [FRONTEND]       errno: -61,
[2026-03-26 19:52:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:52:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:52:13] [FRONTEND]       address: '::1',
[2026-03-26 19:52:13] [FRONTEND]       port: 5001
[2026-03-26 19:52:13] [FRONTEND]     },
[2026-03-26 19:52:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:52:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:52:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:52:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:52:13] [FRONTEND]       errno: -61,
[2026-03-26 19:52:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:52:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:52:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:52:13] [FRONTEND]       port: 5001
[2026-03-26 19:52:13] [FRONTEND]     }
[2026-03-26 19:52:13] [FRONTEND]   ]
[2026-03-26 19:52:13] [FRONTEND] }
[2026-03-26 19:52:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:52:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:52:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:52:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:52:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:52:13] [FRONTEND]   [errors]: [
[2026-03-26 19:52:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:52:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:52:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:52:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:52:13] [FRONTEND]       errno: -61,
[2026-03-26 19:52:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:52:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:52:13] [FRONTEND]       address: '::1',
[2026-03-26 19:52:13] [FRONTEND]       port: 5001
[2026-03-26 19:52:13] [FRONTEND]     },
[2026-03-26 19:52:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:52:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:52:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:52:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:52:13] [FRONTEND]       errno: -61,
[2026-03-26 19:52:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:52:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:52:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:52:13] [FRONTEND]       port: 5001
[2026-03-26 19:52:13] [FRONTEND]     }
[2026-03-26 19:52:13] [FRONTEND]   ]
[2026-03-26 19:52:13] [FRONTEND] }
[2026-03-26 19:53:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:53:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:53:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:53:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:53:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:53:13] [FRONTEND]   [errors]: [
[2026-03-26 19:53:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:53:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:53:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:53:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:53:13] [FRONTEND]       errno: -61,
[2026-03-26 19:53:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:53:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:53:13] [FRONTEND]       address: '::1',
[2026-03-26 19:53:13] [FRONTEND]       port: 5001
[2026-03-26 19:53:13] [FRONTEND]     },
[2026-03-26 19:53:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:53:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:53:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:53:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:53:13] [FRONTEND]       errno: -61,
[2026-03-26 19:53:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:53:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:53:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:53:13] [FRONTEND]       port: 5001
[2026-03-26 19:53:13] [FRONTEND]     }
[2026-03-26 19:53:13] [FRONTEND]   ]
[2026-03-26 19:53:13] [FRONTEND] }
[2026-03-26 19:53:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:53:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:53:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:53:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:53:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:53:13] [FRONTEND]   [errors]: [
[2026-03-26 19:53:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:53:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:53:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:53:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:53:13] [FRONTEND]       errno: -61,
[2026-03-26 19:53:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:53:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:53:13] [FRONTEND]       address: '::1',
[2026-03-26 19:53:13] [FRONTEND]       port: 5001
[2026-03-26 19:53:13] [FRONTEND]     },
[2026-03-26 19:53:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:53:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:53:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:53:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:53:13] [FRONTEND]       errno: -61,
[2026-03-26 19:53:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:53:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:53:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:53:13] [FRONTEND]       port: 5001
[2026-03-26 19:53:13] [FRONTEND]     }
[2026-03-26 19:53:13] [FRONTEND]   ]
[2026-03-26 19:53:13] [FRONTEND] }
[2026-03-26 19:54:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:54:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:54:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:54:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:54:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:54:13] [FRONTEND]   [errors]: [
[2026-03-26 19:54:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:54:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:54:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:54:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:54:13] [FRONTEND]       errno: -61,
[2026-03-26 19:54:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:54:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:54:13] [FRONTEND]       address: '::1',
[2026-03-26 19:54:13] [FRONTEND]       port: 5001
[2026-03-26 19:54:13] [FRONTEND]     },
[2026-03-26 19:54:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:54:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:54:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:54:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:54:13] [FRONTEND]       errno: -61,
[2026-03-26 19:54:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:54:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:54:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:54:13] [FRONTEND]       port: 5001
[2026-03-26 19:54:13] [FRONTEND]     }
[2026-03-26 19:54:13] [FRONTEND]   ]
[2026-03-26 19:54:13] [FRONTEND] }
[2026-03-26 19:54:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:54:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:54:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:54:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:54:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:54:13] [FRONTEND]   [errors]: [
[2026-03-26 19:54:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:54:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:54:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:54:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:54:13] [FRONTEND]       errno: -61,
[2026-03-26 19:54:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:54:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:54:13] [FRONTEND]       address: '::1',
[2026-03-26 19:54:13] [FRONTEND]       port: 5001
[2026-03-26 19:54:13] [FRONTEND]     },
[2026-03-26 19:54:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:54:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:54:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:54:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:54:13] [FRONTEND]       errno: -61,
[2026-03-26 19:54:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:54:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:54:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:54:13] [FRONTEND]       port: 5001
[2026-03-26 19:54:13] [FRONTEND]     }
[2026-03-26 19:54:13] [FRONTEND]   ]
[2026-03-26 19:54:13] [FRONTEND] }
[2026-03-26 19:55:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:55:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:55:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:55:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:55:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:55:13] [FRONTEND]   [errors]: [
[2026-03-26 19:55:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:55:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:55:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:55:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:55:13] [FRONTEND]       errno: -61,
[2026-03-26 19:55:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:55:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:55:13] [FRONTEND]       address: '::1',
[2026-03-26 19:55:13] [FRONTEND]       port: 5001
[2026-03-26 19:55:13] [FRONTEND]     },
[2026-03-26 19:55:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:55:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:55:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:55:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:55:13] [FRONTEND]       errno: -61,
[2026-03-26 19:55:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:55:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:55:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:55:13] [FRONTEND]       port: 5001
[2026-03-26 19:55:13] [FRONTEND]     }
[2026-03-26 19:55:13] [FRONTEND]   ]
[2026-03-26 19:55:13] [FRONTEND] }
[2026-03-26 19:55:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:55:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:55:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:55:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:55:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:55:13] [FRONTEND]   [errors]: [
[2026-03-26 19:55:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:55:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:55:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:55:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:55:13] [FRONTEND]       errno: -61,
[2026-03-26 19:55:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:55:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:55:13] [FRONTEND]       address: '::1',
[2026-03-26 19:55:13] [FRONTEND]       port: 5001
[2026-03-26 19:55:13] [FRONTEND]     },
[2026-03-26 19:55:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:55:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:55:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:55:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:55:13] [FRONTEND]       errno: -61,
[2026-03-26 19:55:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:55:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:55:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:55:13] [FRONTEND]       port: 5001
[2026-03-26 19:55:13] [FRONTEND]     }
[2026-03-26 19:55:13] [FRONTEND]   ]
[2026-03-26 19:55:13] [FRONTEND] }
[2026-03-26 19:56:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:56:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:56:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:56:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:56:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:56:13] [FRONTEND]   [errors]: [
[2026-03-26 19:56:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:56:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:56:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:56:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:56:13] [FRONTEND]       errno: -61,
[2026-03-26 19:56:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:56:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:56:13] [FRONTEND]       address: '::1',
[2026-03-26 19:56:13] [FRONTEND]       port: 5001
[2026-03-26 19:56:13] [FRONTEND]     },
[2026-03-26 19:56:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:56:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:56:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:56:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:56:13] [FRONTEND]       errno: -61,
[2026-03-26 19:56:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:56:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:56:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:56:13] [FRONTEND]       port: 5001
[2026-03-26 19:56:13] [FRONTEND]     }
[2026-03-26 19:56:13] [FRONTEND]   ]
[2026-03-26 19:56:13] [FRONTEND] }
[2026-03-26 19:56:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:56:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:56:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:56:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:56:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:56:13] [FRONTEND]   [errors]: [
[2026-03-26 19:56:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:56:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:56:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:56:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:56:13] [FRONTEND]       errno: -61,
[2026-03-26 19:56:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:56:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:56:13] [FRONTEND]       address: '::1',
[2026-03-26 19:56:13] [FRONTEND]       port: 5001
[2026-03-26 19:56:13] [FRONTEND]     },
[2026-03-26 19:56:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:56:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:56:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:56:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:56:13] [FRONTEND]       errno: -61,
[2026-03-26 19:56:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:56:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:56:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:56:13] [FRONTEND]       port: 5001
[2026-03-26 19:56:13] [FRONTEND]     }
[2026-03-26 19:56:13] [FRONTEND]   ]
[2026-03-26 19:56:13] [FRONTEND] }
[2026-03-26 19:57:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:57:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:57:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:57:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:57:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:57:13] [FRONTEND]   [errors]: [
[2026-03-26 19:57:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:57:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:57:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:57:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:57:13] [FRONTEND]       errno: -61,
[2026-03-26 19:57:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:57:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:57:13] [FRONTEND]       address: '::1',
[2026-03-26 19:57:13] [FRONTEND]       port: 5001
[2026-03-26 19:57:13] [FRONTEND]     },
[2026-03-26 19:57:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:57:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:57:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:57:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:57:13] [FRONTEND]       errno: -61,
[2026-03-26 19:57:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:57:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:57:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:57:13] [FRONTEND]       port: 5001
[2026-03-26 19:57:13] [FRONTEND]     }
[2026-03-26 19:57:13] [FRONTEND]   ]
[2026-03-26 19:57:13] [FRONTEND] }
[2026-03-26 19:57:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:57:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:57:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:57:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:57:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:57:13] [FRONTEND]   [errors]: [
[2026-03-26 19:57:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:57:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:57:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:57:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:57:13] [FRONTEND]       errno: -61,
[2026-03-26 19:57:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:57:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:57:13] [FRONTEND]       address: '::1',
[2026-03-26 19:57:13] [FRONTEND]       port: 5001
[2026-03-26 19:57:13] [FRONTEND]     },
[2026-03-26 19:57:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:57:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:57:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:57:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:57:13] [FRONTEND]       errno: -61,
[2026-03-26 19:57:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:57:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:57:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:57:13] [FRONTEND]       port: 5001
[2026-03-26 19:57:13] [FRONTEND]     }
[2026-03-26 19:57:13] [FRONTEND]   ]
[2026-03-26 19:57:13] [FRONTEND] }
[2026-03-26 19:58:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:58:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:58:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:58:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:58:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:58:13] [FRONTEND]   [errors]: [
[2026-03-26 19:58:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:58:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:58:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:58:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:58:13] [FRONTEND]       errno: -61,
[2026-03-26 19:58:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:58:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:58:13] [FRONTEND]       address: '::1',
[2026-03-26 19:58:13] [FRONTEND]       port: 5001
[2026-03-26 19:58:13] [FRONTEND]     },
[2026-03-26 19:58:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:58:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:58:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:58:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:58:13] [FRONTEND]       errno: -61,
[2026-03-26 19:58:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:58:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:58:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:58:13] [FRONTEND]       port: 5001
[2026-03-26 19:58:13] [FRONTEND]     }
[2026-03-26 19:58:13] [FRONTEND]   ]
[2026-03-26 19:58:13] [FRONTEND] }
[2026-03-26 19:58:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:58:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:58:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:58:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:58:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:58:13] [FRONTEND]   [errors]: [
[2026-03-26 19:58:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:58:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:58:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:58:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:58:13] [FRONTEND]       errno: -61,
[2026-03-26 19:58:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:58:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:58:13] [FRONTEND]       address: '::1',
[2026-03-26 19:58:13] [FRONTEND]       port: 5001
[2026-03-26 19:58:13] [FRONTEND]     },
[2026-03-26 19:58:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:58:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:58:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:58:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:58:13] [FRONTEND]       errno: -61,
[2026-03-26 19:58:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:58:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:58:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:58:13] [FRONTEND]       port: 5001
[2026-03-26 19:58:13] [FRONTEND]     }
[2026-03-26 19:58:13] [FRONTEND]   ]
[2026-03-26 19:58:13] [FRONTEND] }
[2026-03-26 19:59:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 19:59:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:59:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:59:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:59:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:59:13] [FRONTEND]   [errors]: [
[2026-03-26 19:59:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:59:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:59:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:59:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:59:13] [FRONTEND]       errno: -61,
[2026-03-26 19:59:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:59:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:59:13] [FRONTEND]       address: '::1',
[2026-03-26 19:59:13] [FRONTEND]       port: 5001
[2026-03-26 19:59:13] [FRONTEND]     },
[2026-03-26 19:59:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:59:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:59:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:59:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:59:13] [FRONTEND]       errno: -61,
[2026-03-26 19:59:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:59:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:59:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:59:13] [FRONTEND]       port: 5001
[2026-03-26 19:59:13] [FRONTEND]     }
[2026-03-26 19:59:13] [FRONTEND]   ]
[2026-03-26 19:59:13] [FRONTEND] }
[2026-03-26 19:59:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 19:59:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 19:59:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 19:59:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:59:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 19:59:13] [FRONTEND]   [errors]: [
[2026-03-26 19:59:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 19:59:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:59:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:59:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:59:13] [FRONTEND]       errno: -61,
[2026-03-26 19:59:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:59:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:59:13] [FRONTEND]       address: '::1',
[2026-03-26 19:59:13] [FRONTEND]       port: 5001
[2026-03-26 19:59:13] [FRONTEND]     },
[2026-03-26 19:59:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 19:59:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 19:59:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 19:59:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 19:59:13] [FRONTEND]       errno: -61,
[2026-03-26 19:59:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 19:59:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 19:59:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 19:59:13] [FRONTEND]       port: 5001
[2026-03-26 19:59:13] [FRONTEND]     }
[2026-03-26 19:59:13] [FRONTEND]   ]
[2026-03-26 19:59:13] [FRONTEND] }
[2026-03-26 20:00:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:00:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:00:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:00:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:00:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:00:13] [FRONTEND]   [errors]: [
[2026-03-26 20:00:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:00:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:00:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:00:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:00:13] [FRONTEND]       errno: -61,
[2026-03-26 20:00:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:00:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:00:13] [FRONTEND]       address: '::1',
[2026-03-26 20:00:13] [FRONTEND]       port: 5001
[2026-03-26 20:00:13] [FRONTEND]     },
[2026-03-26 20:00:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:00:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:00:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:00:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:00:13] [FRONTEND]       errno: -61,
[2026-03-26 20:00:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:00:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:00:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:00:13] [FRONTEND]       port: 5001
[2026-03-26 20:00:13] [FRONTEND]     }
[2026-03-26 20:00:13] [FRONTEND]   ]
[2026-03-26 20:00:13] [FRONTEND] }
[2026-03-26 20:00:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:00:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:00:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:00:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:00:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:00:13] [FRONTEND]   [errors]: [
[2026-03-26 20:00:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:00:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:00:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:00:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:00:13] [FRONTEND]       errno: -61,
[2026-03-26 20:00:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:00:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:00:13] [FRONTEND]       address: '::1',
[2026-03-26 20:00:13] [FRONTEND]       port: 5001
[2026-03-26 20:00:13] [FRONTEND]     },
[2026-03-26 20:00:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:00:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:00:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:00:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:00:13] [FRONTEND]       errno: -61,
[2026-03-26 20:00:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:00:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:00:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:00:13] [FRONTEND]       port: 5001
[2026-03-26 20:00:13] [FRONTEND]     }
[2026-03-26 20:00:13] [FRONTEND]   ]
[2026-03-26 20:00:13] [FRONTEND] }
[2026-03-26 20:01:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:01:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:01:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:01:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:01:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:01:13] [FRONTEND]   [errors]: [
[2026-03-26 20:01:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:01:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:01:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:01:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:01:13] [FRONTEND]       errno: -61,
[2026-03-26 20:01:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:01:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:01:13] [FRONTEND]       address: '::1',
[2026-03-26 20:01:13] [FRONTEND]       port: 5001
[2026-03-26 20:01:13] [FRONTEND]     },
[2026-03-26 20:01:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:01:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:01:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:01:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:01:13] [FRONTEND]       errno: -61,
[2026-03-26 20:01:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:01:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:01:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:01:13] [FRONTEND]       port: 5001
[2026-03-26 20:01:13] [FRONTEND]     }
[2026-03-26 20:01:13] [FRONTEND]   ]
[2026-03-26 20:01:13] [FRONTEND] }
[2026-03-26 20:01:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:01:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:01:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:01:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:01:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:01:13] [FRONTEND]   [errors]: [
[2026-03-26 20:01:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:01:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:01:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:01:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:01:13] [FRONTEND]       errno: -61,
[2026-03-26 20:01:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:01:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:01:13] [FRONTEND]       address: '::1',
[2026-03-26 20:01:13] [FRONTEND]       port: 5001
[2026-03-26 20:01:13] [FRONTEND]     },
[2026-03-26 20:01:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:01:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:01:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:01:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:01:13] [FRONTEND]       errno: -61,
[2026-03-26 20:01:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:01:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:01:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:01:13] [FRONTEND]       port: 5001
[2026-03-26 20:01:13] [FRONTEND]     }
[2026-03-26 20:01:13] [FRONTEND]   ]
[2026-03-26 20:01:13] [FRONTEND] }
[2026-03-26 20:02:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:02:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:02:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:02:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:02:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:02:13] [FRONTEND]   [errors]: [
[2026-03-26 20:02:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:02:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:02:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:02:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:02:13] [FRONTEND]       errno: -61,
[2026-03-26 20:02:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:02:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:02:13] [FRONTEND]       address: '::1',
[2026-03-26 20:02:13] [FRONTEND]       port: 5001
[2026-03-26 20:02:13] [FRONTEND]     },
[2026-03-26 20:02:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:02:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:02:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:02:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:02:13] [FRONTEND]       errno: -61,
[2026-03-26 20:02:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:02:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:02:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:02:13] [FRONTEND]       port: 5001
[2026-03-26 20:02:13] [FRONTEND]     }
[2026-03-26 20:02:13] [FRONTEND]   ]
[2026-03-26 20:02:13] [FRONTEND] }
[2026-03-26 20:02:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:02:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:02:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:02:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:02:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:02:13] [FRONTEND]   [errors]: [
[2026-03-26 20:02:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:02:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:02:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:02:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:02:13] [FRONTEND]       errno: -61,
[2026-03-26 20:02:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:02:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:02:13] [FRONTEND]       address: '::1',
[2026-03-26 20:02:13] [FRONTEND]       port: 5001
[2026-03-26 20:02:13] [FRONTEND]     },
[2026-03-26 20:02:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:02:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:02:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:02:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:02:13] [FRONTEND]       errno: -61,
[2026-03-26 20:02:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:02:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:02:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:02:13] [FRONTEND]       port: 5001
[2026-03-26 20:02:13] [FRONTEND]     }
[2026-03-26 20:02:13] [FRONTEND]   ]
[2026-03-26 20:02:13] [FRONTEND] }
[2026-03-26 20:03:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:03:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:03:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:03:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:03:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:03:13] [FRONTEND]   [errors]: [
[2026-03-26 20:03:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:03:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:03:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:03:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:03:13] [FRONTEND]       errno: -61,
[2026-03-26 20:03:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:03:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:03:13] [FRONTEND]       address: '::1',
[2026-03-26 20:03:13] [FRONTEND]       port: 5001
[2026-03-26 20:03:13] [FRONTEND]     },
[2026-03-26 20:03:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:03:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:03:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:03:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:03:13] [FRONTEND]       errno: -61,
[2026-03-26 20:03:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:03:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:03:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:03:13] [FRONTEND]       port: 5001
[2026-03-26 20:03:13] [FRONTEND]     }
[2026-03-26 20:03:13] [FRONTEND]   ]
[2026-03-26 20:03:13] [FRONTEND] }
[2026-03-26 20:03:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:03:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:03:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:03:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:03:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:03:13] [FRONTEND]   [errors]: [
[2026-03-26 20:03:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:03:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:03:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:03:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:03:13] [FRONTEND]       errno: -61,
[2026-03-26 20:03:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:03:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:03:13] [FRONTEND]       address: '::1',
[2026-03-26 20:03:13] [FRONTEND]       port: 5001
[2026-03-26 20:03:13] [FRONTEND]     },
[2026-03-26 20:03:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:03:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:03:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:03:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:03:13] [FRONTEND]       errno: -61,
[2026-03-26 20:03:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:03:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:03:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:03:13] [FRONTEND]       port: 5001
[2026-03-26 20:03:13] [FRONTEND]     }
[2026-03-26 20:03:13] [FRONTEND]   ]
[2026-03-26 20:03:13] [FRONTEND] }
[2026-03-26 20:04:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:04:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:04:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:04:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:04:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:04:13] [FRONTEND]   [errors]: [
[2026-03-26 20:04:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:04:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:04:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:04:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:04:13] [FRONTEND]       errno: -61,
[2026-03-26 20:04:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:04:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:04:13] [FRONTEND]       address: '::1',
[2026-03-26 20:04:13] [FRONTEND]       port: 5001
[2026-03-26 20:04:13] [FRONTEND]     },
[2026-03-26 20:04:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:04:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:04:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:04:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:04:13] [FRONTEND]       errno: -61,
[2026-03-26 20:04:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:04:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:04:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:04:13] [FRONTEND]       port: 5001
[2026-03-26 20:04:13] [FRONTEND]     }
[2026-03-26 20:04:13] [FRONTEND]   ]
[2026-03-26 20:04:13] [FRONTEND] }
[2026-03-26 20:04:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:04:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:04:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:04:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:04:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:04:13] [FRONTEND]   [errors]: [
[2026-03-26 20:04:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:04:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:04:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:04:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:04:13] [FRONTEND]       errno: -61,
[2026-03-26 20:04:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:04:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:04:13] [FRONTEND]       address: '::1',
[2026-03-26 20:04:13] [FRONTEND]       port: 5001
[2026-03-26 20:04:13] [FRONTEND]     },
[2026-03-26 20:04:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:04:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:04:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:04:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:04:13] [FRONTEND]       errno: -61,
[2026-03-26 20:04:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:04:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:04:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:04:13] [FRONTEND]       port: 5001
[2026-03-26 20:04:13] [FRONTEND]     }
[2026-03-26 20:04:13] [FRONTEND]   ]
[2026-03-26 20:04:13] [FRONTEND] }
[2026-03-26 20:05:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:05:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:05:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:05:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:05:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:05:13] [FRONTEND]   [errors]: [
[2026-03-26 20:05:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:05:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:05:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:05:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:05:13] [FRONTEND]       errno: -61,
[2026-03-26 20:05:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:05:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:05:13] [FRONTEND]       address: '::1',
[2026-03-26 20:05:13] [FRONTEND]       port: 5001
[2026-03-26 20:05:13] [FRONTEND]     },
[2026-03-26 20:05:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:05:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:05:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:05:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:05:13] [FRONTEND]       errno: -61,
[2026-03-26 20:05:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:05:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:05:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:05:13] [FRONTEND]       port: 5001
[2026-03-26 20:05:13] [FRONTEND]     }
[2026-03-26 20:05:13] [FRONTEND]   ]
[2026-03-26 20:05:13] [FRONTEND] }
[2026-03-26 20:05:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:05:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:05:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:05:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:05:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:05:13] [FRONTEND]   [errors]: [
[2026-03-26 20:05:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:05:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:05:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:05:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:05:13] [FRONTEND]       errno: -61,
[2026-03-26 20:05:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:05:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:05:13] [FRONTEND]       address: '::1',
[2026-03-26 20:05:13] [FRONTEND]       port: 5001
[2026-03-26 20:05:13] [FRONTEND]     },
[2026-03-26 20:05:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:05:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:05:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:05:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:05:13] [FRONTEND]       errno: -61,
[2026-03-26 20:05:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:05:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:05:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:05:13] [FRONTEND]       port: 5001
[2026-03-26 20:05:13] [FRONTEND]     }
[2026-03-26 20:05:13] [FRONTEND]   ]
[2026-03-26 20:05:13] [FRONTEND] }
[2026-03-26 20:06:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:06:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:06:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:06:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:06:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:06:13] [FRONTEND]   [errors]: [
[2026-03-26 20:06:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:06:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:06:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:06:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:06:13] [FRONTEND]       errno: -61,
[2026-03-26 20:06:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:06:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:06:13] [FRONTEND]       address: '::1',
[2026-03-26 20:06:13] [FRONTEND]       port: 5001
[2026-03-26 20:06:13] [FRONTEND]     },
[2026-03-26 20:06:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:06:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:06:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:06:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:06:13] [FRONTEND]       errno: -61,
[2026-03-26 20:06:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:06:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:06:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:06:13] [FRONTEND]       port: 5001
[2026-03-26 20:06:13] [FRONTEND]     }
[2026-03-26 20:06:13] [FRONTEND]   ]
[2026-03-26 20:06:13] [FRONTEND] }
[2026-03-26 20:06:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:06:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:06:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:06:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:06:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:06:13] [FRONTEND]   [errors]: [
[2026-03-26 20:06:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:06:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:06:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:06:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:06:13] [FRONTEND]       errno: -61,
[2026-03-26 20:06:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:06:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:06:13] [FRONTEND]       address: '::1',
[2026-03-26 20:06:13] [FRONTEND]       port: 5001
[2026-03-26 20:06:13] [FRONTEND]     },
[2026-03-26 20:06:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:06:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:06:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:06:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:06:13] [FRONTEND]       errno: -61,
[2026-03-26 20:06:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:06:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:06:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:06:13] [FRONTEND]       port: 5001
[2026-03-26 20:06:13] [FRONTEND]     }
[2026-03-26 20:06:13] [FRONTEND]   ]
[2026-03-26 20:06:13] [FRONTEND] }
[2026-03-26 20:07:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:07:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:07:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:07:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:07:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:07:13] [FRONTEND]   [errors]: [
[2026-03-26 20:07:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:07:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:07:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:07:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:07:13] [FRONTEND]       errno: -61,
[2026-03-26 20:07:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:07:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:07:13] [FRONTEND]       address: '::1',
[2026-03-26 20:07:13] [FRONTEND]       port: 5001
[2026-03-26 20:07:13] [FRONTEND]     },
[2026-03-26 20:07:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:07:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:07:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:07:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:07:13] [FRONTEND]       errno: -61,
[2026-03-26 20:07:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:07:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:07:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:07:13] [FRONTEND]       port: 5001
[2026-03-26 20:07:13] [FRONTEND]     }
[2026-03-26 20:07:13] [FRONTEND]   ]
[2026-03-26 20:07:13] [FRONTEND] }
[2026-03-26 20:07:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:07:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:07:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:07:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:07:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:07:13] [FRONTEND]   [errors]: [
[2026-03-26 20:07:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:07:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:07:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:07:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:07:13] [FRONTEND]       errno: -61,
[2026-03-26 20:07:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:07:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:07:13] [FRONTEND]       address: '::1',
[2026-03-26 20:07:13] [FRONTEND]       port: 5001
[2026-03-26 20:07:13] [FRONTEND]     },
[2026-03-26 20:07:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:07:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:07:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:07:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:07:13] [FRONTEND]       errno: -61,
[2026-03-26 20:07:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:07:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:07:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:07:13] [FRONTEND]       port: 5001
[2026-03-26 20:07:13] [FRONTEND]     }
[2026-03-26 20:07:13] [FRONTEND]   ]
[2026-03-26 20:07:13] [FRONTEND] }
[2026-03-26 20:08:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:08:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:08:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:08:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:08:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:08:13] [FRONTEND]   [errors]: [
[2026-03-26 20:08:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:08:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:08:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:08:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:08:13] [FRONTEND]       errno: -61,
[2026-03-26 20:08:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:08:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:08:13] [FRONTEND]       address: '::1',
[2026-03-26 20:08:13] [FRONTEND]       port: 5001
[2026-03-26 20:08:13] [FRONTEND]     },
[2026-03-26 20:08:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:08:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:08:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:08:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:08:13] [FRONTEND]       errno: -61,
[2026-03-26 20:08:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:08:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:08:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:08:13] [FRONTEND]       port: 5001
[2026-03-26 20:08:13] [FRONTEND]     }
[2026-03-26 20:08:13] [FRONTEND]   ]
[2026-03-26 20:08:13] [FRONTEND] }
[2026-03-26 20:08:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:08:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:08:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:08:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:08:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:08:13] [FRONTEND]   [errors]: [
[2026-03-26 20:08:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:08:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:08:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:08:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:08:13] [FRONTEND]       errno: -61,
[2026-03-26 20:08:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:08:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:08:13] [FRONTEND]       address: '::1',
[2026-03-26 20:08:13] [FRONTEND]       port: 5001
[2026-03-26 20:08:13] [FRONTEND]     },
[2026-03-26 20:08:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:08:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:08:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:08:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:08:13] [FRONTEND]       errno: -61,
[2026-03-26 20:08:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:08:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:08:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:08:13] [FRONTEND]       port: 5001
[2026-03-26 20:08:13] [FRONTEND]     }
[2026-03-26 20:08:13] [FRONTEND]   ]
[2026-03-26 20:08:13] [FRONTEND] }
[2026-03-26 20:09:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:09:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:09:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:09:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:09:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:09:13] [FRONTEND]   [errors]: [
[2026-03-26 20:09:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:09:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:09:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:09:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:09:13] [FRONTEND]       errno: -61,
[2026-03-26 20:09:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:09:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:09:13] [FRONTEND]       address: '::1',
[2026-03-26 20:09:13] [FRONTEND]       port: 5001
[2026-03-26 20:09:13] [FRONTEND]     },
[2026-03-26 20:09:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:09:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:09:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:09:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:09:13] [FRONTEND]       errno: -61,
[2026-03-26 20:09:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:09:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:09:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:09:13] [FRONTEND]       port: 5001
[2026-03-26 20:09:13] [FRONTEND]     }
[2026-03-26 20:09:13] [FRONTEND]   ]
[2026-03-26 20:09:13] [FRONTEND] }
[2026-03-26 20:09:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:09:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:09:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:09:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:09:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:09:13] [FRONTEND]   [errors]: [
[2026-03-26 20:09:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:09:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:09:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:09:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:09:13] [FRONTEND]       errno: -61,
[2026-03-26 20:09:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:09:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:09:13] [FRONTEND]       address: '::1',
[2026-03-26 20:09:13] [FRONTEND]       port: 5001
[2026-03-26 20:09:13] [FRONTEND]     },
[2026-03-26 20:09:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:09:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:09:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:09:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:09:13] [FRONTEND]       errno: -61,
[2026-03-26 20:09:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:09:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:09:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:09:13] [FRONTEND]       port: 5001
[2026-03-26 20:09:13] [FRONTEND]     }
[2026-03-26 20:09:13] [FRONTEND]   ]
[2026-03-26 20:09:13] [FRONTEND] }
[2026-03-26 20:10:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:10:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:10:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:10:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:10:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:10:13] [FRONTEND]   [errors]: [
[2026-03-26 20:10:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:10:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:10:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:10:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:10:13] [FRONTEND]       errno: -61,
[2026-03-26 20:10:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:10:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:10:13] [FRONTEND]       address: '::1',
[2026-03-26 20:10:13] [FRONTEND]       port: 5001
[2026-03-26 20:10:13] [FRONTEND]     },
[2026-03-26 20:10:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:10:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:10:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:10:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:10:13] [FRONTEND]       errno: -61,
[2026-03-26 20:10:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:10:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:10:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:10:13] [FRONTEND]       port: 5001
[2026-03-26 20:10:13] [FRONTEND]     }
[2026-03-26 20:10:13] [FRONTEND]   ]
[2026-03-26 20:10:13] [FRONTEND] }
[2026-03-26 20:10:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:10:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:10:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:10:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:10:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:10:13] [FRONTEND]   [errors]: [
[2026-03-26 20:10:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:10:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:10:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:10:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:10:13] [FRONTEND]       errno: -61,
[2026-03-26 20:10:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:10:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:10:13] [FRONTEND]       address: '::1',
[2026-03-26 20:10:13] [FRONTEND]       port: 5001
[2026-03-26 20:10:13] [FRONTEND]     },
[2026-03-26 20:10:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:10:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:10:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:10:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:10:13] [FRONTEND]       errno: -61,
[2026-03-26 20:10:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:10:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:10:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:10:13] [FRONTEND]       port: 5001
[2026-03-26 20:10:13] [FRONTEND]     }
[2026-03-26 20:10:13] [FRONTEND]   ]
[2026-03-26 20:10:13] [FRONTEND] }
[2026-03-26 20:11:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:11:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:11:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:11:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:11:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:11:13] [FRONTEND]   [errors]: [
[2026-03-26 20:11:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:11:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:11:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:11:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:11:13] [FRONTEND]       errno: -61,
[2026-03-26 20:11:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:11:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:11:13] [FRONTEND]       address: '::1',
[2026-03-26 20:11:13] [FRONTEND]       port: 5001
[2026-03-26 20:11:13] [FRONTEND]     },
[2026-03-26 20:11:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:11:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:11:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:11:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:11:13] [FRONTEND]       errno: -61,
[2026-03-26 20:11:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:11:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:11:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:11:13] [FRONTEND]       port: 5001
[2026-03-26 20:11:13] [FRONTEND]     }
[2026-03-26 20:11:13] [FRONTEND]   ]
[2026-03-26 20:11:13] [FRONTEND] }
[2026-03-26 20:11:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:11:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:11:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:11:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:11:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:11:13] [FRONTEND]   [errors]: [
[2026-03-26 20:11:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:11:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:11:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:11:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:11:13] [FRONTEND]       errno: -61,
[2026-03-26 20:11:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:11:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:11:13] [FRONTEND]       address: '::1',
[2026-03-26 20:11:13] [FRONTEND]       port: 5001
[2026-03-26 20:11:13] [FRONTEND]     },
[2026-03-26 20:11:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:11:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:11:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:11:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:11:13] [FRONTEND]       errno: -61,
[2026-03-26 20:11:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:11:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:11:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:11:13] [FRONTEND]       port: 5001
[2026-03-26 20:11:13] [FRONTEND]     }
[2026-03-26 20:11:13] [FRONTEND]   ]
[2026-03-26 20:11:13] [FRONTEND] }
[2026-03-26 20:12:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:12:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:12:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:12:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:12:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:12:13] [FRONTEND]   [errors]: [
[2026-03-26 20:12:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:12:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:12:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:12:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:12:13] [FRONTEND]       errno: -61,
[2026-03-26 20:12:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:12:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:12:13] [FRONTEND]       address: '::1',
[2026-03-26 20:12:13] [FRONTEND]       port: 5001
[2026-03-26 20:12:13] [FRONTEND]     },
[2026-03-26 20:12:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:12:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:12:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:12:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:12:13] [FRONTEND]       errno: -61,
[2026-03-26 20:12:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:12:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:12:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:12:13] [FRONTEND]       port: 5001
[2026-03-26 20:12:13] [FRONTEND]     }
[2026-03-26 20:12:13] [FRONTEND]   ]
[2026-03-26 20:12:13] [FRONTEND] }
[2026-03-26 20:12:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:12:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:12:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:12:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:12:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:12:13] [FRONTEND]   [errors]: [
[2026-03-26 20:12:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:12:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:12:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:12:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:12:13] [FRONTEND]       errno: -61,
[2026-03-26 20:12:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:12:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:12:13] [FRONTEND]       address: '::1',
[2026-03-26 20:12:13] [FRONTEND]       port: 5001
[2026-03-26 20:12:13] [FRONTEND]     },
[2026-03-26 20:12:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:12:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:12:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:12:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:12:13] [FRONTEND]       errno: -61,
[2026-03-26 20:12:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:12:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:12:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:12:13] [FRONTEND]       port: 5001
[2026-03-26 20:12:13] [FRONTEND]     }
[2026-03-26 20:12:13] [FRONTEND]   ]
[2026-03-26 20:12:13] [FRONTEND] }
[2026-03-26 20:13:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:13:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:13:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:13:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:13:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:13:13] [FRONTEND]   [errors]: [
[2026-03-26 20:13:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:13:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:13:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:13:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:13:13] [FRONTEND]       errno: -61,
[2026-03-26 20:13:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:13:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:13:13] [FRONTEND]       address: '::1',
[2026-03-26 20:13:13] [FRONTEND]       port: 5001
[2026-03-26 20:13:13] [FRONTEND]     },
[2026-03-26 20:13:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:13:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:13:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:13:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:13:13] [FRONTEND]       errno: -61,
[2026-03-26 20:13:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:13:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:13:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:13:13] [FRONTEND]       port: 5001
[2026-03-26 20:13:13] [FRONTEND]     }
[2026-03-26 20:13:13] [FRONTEND]   ]
[2026-03-26 20:13:13] [FRONTEND] }
[2026-03-26 20:13:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:13:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:13:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:13:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:13:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:13:13] [FRONTEND]   [errors]: [
[2026-03-26 20:13:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:13:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:13:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:13:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:13:13] [FRONTEND]       errno: -61,
[2026-03-26 20:13:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:13:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:13:13] [FRONTEND]       address: '::1',
[2026-03-26 20:13:13] [FRONTEND]       port: 5001
[2026-03-26 20:13:13] [FRONTEND]     },
[2026-03-26 20:13:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:13:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:13:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:13:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:13:13] [FRONTEND]       errno: -61,
[2026-03-26 20:13:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:13:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:13:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:13:13] [FRONTEND]       port: 5001
[2026-03-26 20:13:13] [FRONTEND]     }
[2026-03-26 20:13:13] [FRONTEND]   ]
[2026-03-26 20:13:13] [FRONTEND] }
[2026-03-26 20:14:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:14:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:14:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:14:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:14:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:14:13] [FRONTEND]   [errors]: [
[2026-03-26 20:14:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:14:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:14:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:14:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:14:13] [FRONTEND]       errno: -61,
[2026-03-26 20:14:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:14:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:14:13] [FRONTEND]       address: '::1',
[2026-03-26 20:14:13] [FRONTEND]       port: 5001
[2026-03-26 20:14:13] [FRONTEND]     },
[2026-03-26 20:14:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:14:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:14:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:14:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:14:13] [FRONTEND]       errno: -61,
[2026-03-26 20:14:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:14:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:14:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:14:13] [FRONTEND]       port: 5001
[2026-03-26 20:14:13] [FRONTEND]     }
[2026-03-26 20:14:13] [FRONTEND]   ]
[2026-03-26 20:14:13] [FRONTEND] }
[2026-03-26 20:14:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:14:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:14:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:14:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:14:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:14:13] [FRONTEND]   [errors]: [
[2026-03-26 20:14:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:14:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:14:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:14:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:14:13] [FRONTEND]       errno: -61,
[2026-03-26 20:14:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:14:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:14:13] [FRONTEND]       address: '::1',
[2026-03-26 20:14:13] [FRONTEND]       port: 5001
[2026-03-26 20:14:13] [FRONTEND]     },
[2026-03-26 20:14:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:14:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:14:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:14:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:14:13] [FRONTEND]       errno: -61,
[2026-03-26 20:14:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:14:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:14:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:14:13] [FRONTEND]       port: 5001
[2026-03-26 20:14:13] [FRONTEND]     }
[2026-03-26 20:14:13] [FRONTEND]   ]
[2026-03-26 20:14:13] [FRONTEND] }
[2026-03-26 20:15:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:15:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:15:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:15:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:15:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:15:13] [FRONTEND]   [errors]: [
[2026-03-26 20:15:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:15:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:15:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:15:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:15:13] [FRONTEND]       errno: -61,
[2026-03-26 20:15:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:15:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:15:13] [FRONTEND]       address: '::1',
[2026-03-26 20:15:13] [FRONTEND]       port: 5001
[2026-03-26 20:15:13] [FRONTEND]     },
[2026-03-26 20:15:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:15:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:15:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:15:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:15:13] [FRONTEND]       errno: -61,
[2026-03-26 20:15:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:15:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:15:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:15:13] [FRONTEND]       port: 5001
[2026-03-26 20:15:13] [FRONTEND]     }
[2026-03-26 20:15:13] [FRONTEND]   ]
[2026-03-26 20:15:13] [FRONTEND] }
[2026-03-26 20:15:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:15:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:15:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:15:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:15:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:15:13] [FRONTEND]   [errors]: [
[2026-03-26 20:15:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:15:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:15:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:15:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:15:13] [FRONTEND]       errno: -61,
[2026-03-26 20:15:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:15:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:15:13] [FRONTEND]       address: '::1',
[2026-03-26 20:15:13] [FRONTEND]       port: 5001
[2026-03-26 20:15:13] [FRONTEND]     },
[2026-03-26 20:15:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:15:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:15:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:15:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:15:13] [FRONTEND]       errno: -61,
[2026-03-26 20:15:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:15:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:15:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:15:13] [FRONTEND]       port: 5001
[2026-03-26 20:15:13] [FRONTEND]     }
[2026-03-26 20:15:13] [FRONTEND]   ]
[2026-03-26 20:15:13] [FRONTEND] }
[2026-03-26 20:16:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:16:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:16:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:16:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:16:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:16:13] [FRONTEND]   [errors]: [
[2026-03-26 20:16:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:16:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:16:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:16:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:16:13] [FRONTEND]       errno: -61,
[2026-03-26 20:16:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:16:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:16:13] [FRONTEND]       address: '::1',
[2026-03-26 20:16:13] [FRONTEND]       port: 5001
[2026-03-26 20:16:13] [FRONTEND]     },
[2026-03-26 20:16:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:16:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:16:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:16:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:16:13] [FRONTEND]       errno: -61,
[2026-03-26 20:16:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:16:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:16:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:16:13] [FRONTEND]       port: 5001
[2026-03-26 20:16:13] [FRONTEND]     }
[2026-03-26 20:16:13] [FRONTEND]   ]
[2026-03-26 20:16:13] [FRONTEND] }
[2026-03-26 20:16:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:16:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:16:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:16:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:16:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:16:13] [FRONTEND]   [errors]: [
[2026-03-26 20:16:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:16:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:16:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:16:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:16:13] [FRONTEND]       errno: -61,
[2026-03-26 20:16:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:16:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:16:13] [FRONTEND]       address: '::1',
[2026-03-26 20:16:13] [FRONTEND]       port: 5001
[2026-03-26 20:16:13] [FRONTEND]     },
[2026-03-26 20:16:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:16:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:16:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:16:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:16:13] [FRONTEND]       errno: -61,
[2026-03-26 20:16:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:16:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:16:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:16:13] [FRONTEND]       port: 5001
[2026-03-26 20:16:13] [FRONTEND]     }
[2026-03-26 20:16:13] [FRONTEND]   ]
[2026-03-26 20:16:13] [FRONTEND] }
[2026-03-26 20:17:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:17:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:17:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:17:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:17:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:17:13] [FRONTEND]   [errors]: [
[2026-03-26 20:17:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:17:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:17:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:17:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:17:13] [FRONTEND]       errno: -61,
[2026-03-26 20:17:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:17:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:17:13] [FRONTEND]       address: '::1',
[2026-03-26 20:17:13] [FRONTEND]       port: 5001
[2026-03-26 20:17:13] [FRONTEND]     },
[2026-03-26 20:17:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:17:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:17:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:17:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:17:13] [FRONTEND]       errno: -61,
[2026-03-26 20:17:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:17:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:17:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:17:13] [FRONTEND]       port: 5001
[2026-03-26 20:17:13] [FRONTEND]     }
[2026-03-26 20:17:13] [FRONTEND]   ]
[2026-03-26 20:17:13] [FRONTEND] }
[2026-03-26 20:17:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:17:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:17:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:17:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:17:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:17:13] [FRONTEND]   [errors]: [
[2026-03-26 20:17:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:17:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:17:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:17:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:17:13] [FRONTEND]       errno: -61,
[2026-03-26 20:17:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:17:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:17:13] [FRONTEND]       address: '::1',
[2026-03-26 20:17:13] [FRONTEND]       port: 5001
[2026-03-26 20:17:13] [FRONTEND]     },
[2026-03-26 20:17:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:17:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:17:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:17:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:17:13] [FRONTEND]       errno: -61,
[2026-03-26 20:17:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:17:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:17:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:17:13] [FRONTEND]       port: 5001
[2026-03-26 20:17:13] [FRONTEND]     }
[2026-03-26 20:17:13] [FRONTEND]   ]
[2026-03-26 20:17:13] [FRONTEND] }
[2026-03-26 20:18:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:18:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:18:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:18:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:18:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:18:13] [FRONTEND]   [errors]: [
[2026-03-26 20:18:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:18:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:18:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:18:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:18:13] [FRONTEND]       errno: -61,
[2026-03-26 20:18:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:18:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:18:13] [FRONTEND]       address: '::1',
[2026-03-26 20:18:13] [FRONTEND]       port: 5001
[2026-03-26 20:18:13] [FRONTEND]     },
[2026-03-26 20:18:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:18:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:18:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:18:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:18:13] [FRONTEND]       errno: -61,
[2026-03-26 20:18:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:18:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:18:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:18:13] [FRONTEND]       port: 5001
[2026-03-26 20:18:13] [FRONTEND]     }
[2026-03-26 20:18:13] [FRONTEND]   ]
[2026-03-26 20:18:13] [FRONTEND] }
[2026-03-26 20:18:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:18:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:18:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:18:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:18:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:18:13] [FRONTEND]   [errors]: [
[2026-03-26 20:18:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:18:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:18:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:18:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:18:13] [FRONTEND]       errno: -61,
[2026-03-26 20:18:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:18:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:18:13] [FRONTEND]       address: '::1',
[2026-03-26 20:18:13] [FRONTEND]       port: 5001
[2026-03-26 20:18:13] [FRONTEND]     },
[2026-03-26 20:18:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:18:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:18:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:18:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:18:13] [FRONTEND]       errno: -61,
[2026-03-26 20:18:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:18:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:18:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:18:13] [FRONTEND]       port: 5001
[2026-03-26 20:18:13] [FRONTEND]     }
[2026-03-26 20:18:13] [FRONTEND]   ]
[2026-03-26 20:18:13] [FRONTEND] }
[2026-03-26 20:19:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:19:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:19:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:19:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:19:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:19:13] [FRONTEND]   [errors]: [
[2026-03-26 20:19:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:19:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:19:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:19:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:19:13] [FRONTEND]       errno: -61,
[2026-03-26 20:19:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:19:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:19:13] [FRONTEND]       address: '::1',
[2026-03-26 20:19:13] [FRONTEND]       port: 5001
[2026-03-26 20:19:13] [FRONTEND]     },
[2026-03-26 20:19:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:19:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:19:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:19:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:19:13] [FRONTEND]       errno: -61,
[2026-03-26 20:19:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:19:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:19:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:19:13] [FRONTEND]       port: 5001
[2026-03-26 20:19:13] [FRONTEND]     }
[2026-03-26 20:19:13] [FRONTEND]   ]
[2026-03-26 20:19:13] [FRONTEND] }
[2026-03-26 20:19:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:19:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:19:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:19:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:19:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:19:13] [FRONTEND]   [errors]: [
[2026-03-26 20:19:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:19:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:19:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:19:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:19:13] [FRONTEND]       errno: -61,
[2026-03-26 20:19:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:19:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:19:13] [FRONTEND]       address: '::1',
[2026-03-26 20:19:13] [FRONTEND]       port: 5001
[2026-03-26 20:19:13] [FRONTEND]     },
[2026-03-26 20:19:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:19:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:19:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:19:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:19:13] [FRONTEND]       errno: -61,
[2026-03-26 20:19:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:19:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:19:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:19:13] [FRONTEND]       port: 5001
[2026-03-26 20:19:13] [FRONTEND]     }
[2026-03-26 20:19:13] [FRONTEND]   ]
[2026-03-26 20:19:13] [FRONTEND] }
[2026-03-26 20:20:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:20:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:20:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:20:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:20:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:20:13] [FRONTEND]   [errors]: [
[2026-03-26 20:20:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:20:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:20:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:20:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:20:13] [FRONTEND]       errno: -61,
[2026-03-26 20:20:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:20:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:20:13] [FRONTEND]       address: '::1',
[2026-03-26 20:20:13] [FRONTEND]       port: 5001
[2026-03-26 20:20:13] [FRONTEND]     },
[2026-03-26 20:20:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:20:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:20:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:20:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:20:13] [FRONTEND]       errno: -61,
[2026-03-26 20:20:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:20:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:20:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:20:13] [FRONTEND]       port: 5001
[2026-03-26 20:20:13] [FRONTEND]     }
[2026-03-26 20:20:13] [FRONTEND]   ]
[2026-03-26 20:20:13] [FRONTEND] }
[2026-03-26 20:20:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:20:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:20:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:20:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:20:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:20:13] [FRONTEND]   [errors]: [
[2026-03-26 20:20:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:20:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:20:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:20:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:20:13] [FRONTEND]       errno: -61,
[2026-03-26 20:20:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:20:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:20:13] [FRONTEND]       address: '::1',
[2026-03-26 20:20:13] [FRONTEND]       port: 5001
[2026-03-26 20:20:13] [FRONTEND]     },
[2026-03-26 20:20:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:20:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:20:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:20:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:20:13] [FRONTEND]       errno: -61,
[2026-03-26 20:20:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:20:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:20:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:20:13] [FRONTEND]       port: 5001
[2026-03-26 20:20:13] [FRONTEND]     }
[2026-03-26 20:20:13] [FRONTEND]   ]
[2026-03-26 20:20:13] [FRONTEND] }
[2026-03-26 20:21:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:21:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:21:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:21:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:21:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:21:13] [FRONTEND]   [errors]: [
[2026-03-26 20:21:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:21:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:21:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:21:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:21:13] [FRONTEND]       errno: -61,
[2026-03-26 20:21:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:21:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:21:13] [FRONTEND]       address: '::1',
[2026-03-26 20:21:13] [FRONTEND]       port: 5001
[2026-03-26 20:21:13] [FRONTEND]     },
[2026-03-26 20:21:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:21:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:21:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:21:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:21:13] [FRONTEND]       errno: -61,
[2026-03-26 20:21:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:21:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:21:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:21:13] [FRONTEND]       port: 5001
[2026-03-26 20:21:13] [FRONTEND]     }
[2026-03-26 20:21:13] [FRONTEND]   ]
[2026-03-26 20:21:13] [FRONTEND] }
[2026-03-26 20:21:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:21:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:21:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:21:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:21:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:21:13] [FRONTEND]   [errors]: [
[2026-03-26 20:21:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:21:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:21:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:21:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:21:13] [FRONTEND]       errno: -61,
[2026-03-26 20:21:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:21:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:21:13] [FRONTEND]       address: '::1',
[2026-03-26 20:21:13] [FRONTEND]       port: 5001
[2026-03-26 20:21:13] [FRONTEND]     },
[2026-03-26 20:21:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:21:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:21:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:21:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:21:13] [FRONTEND]       errno: -61,
[2026-03-26 20:21:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:21:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:21:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:21:13] [FRONTEND]       port: 5001
[2026-03-26 20:21:13] [FRONTEND]     }
[2026-03-26 20:21:13] [FRONTEND]   ]
[2026-03-26 20:21:13] [FRONTEND] }
[2026-03-26 20:22:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:22:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:22:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:22:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:22:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:22:13] [FRONTEND]   [errors]: [
[2026-03-26 20:22:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:22:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:22:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:22:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:22:13] [FRONTEND]       errno: -61,
[2026-03-26 20:22:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:22:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:22:13] [FRONTEND]       address: '::1',
[2026-03-26 20:22:13] [FRONTEND]       port: 5001
[2026-03-26 20:22:13] [FRONTEND]     },
[2026-03-26 20:22:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:22:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:22:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:22:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:22:13] [FRONTEND]       errno: -61,
[2026-03-26 20:22:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:22:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:22:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:22:13] [FRONTEND]       port: 5001
[2026-03-26 20:22:13] [FRONTEND]     }
[2026-03-26 20:22:13] [FRONTEND]   ]
[2026-03-26 20:22:13] [FRONTEND] }
[2026-03-26 20:22:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:22:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:22:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:22:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:22:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:22:13] [FRONTEND]   [errors]: [
[2026-03-26 20:22:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:22:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:22:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:22:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:22:13] [FRONTEND]       errno: -61,
[2026-03-26 20:22:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:22:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:22:13] [FRONTEND]       address: '::1',
[2026-03-26 20:22:13] [FRONTEND]       port: 5001
[2026-03-26 20:22:13] [FRONTEND]     },
[2026-03-26 20:22:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:22:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:22:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:22:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:22:13] [FRONTEND]       errno: -61,
[2026-03-26 20:22:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:22:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:22:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:22:13] [FRONTEND]       port: 5001
[2026-03-26 20:22:13] [FRONTEND]     }
[2026-03-26 20:22:13] [FRONTEND]   ]
[2026-03-26 20:22:13] [FRONTEND] }
[2026-03-26 20:23:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:23:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:23:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:23:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:23:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:23:13] [FRONTEND]   [errors]: [
[2026-03-26 20:23:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:23:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:23:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:23:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:23:13] [FRONTEND]       errno: -61,
[2026-03-26 20:23:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:23:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:23:13] [FRONTEND]       address: '::1',
[2026-03-26 20:23:13] [FRONTEND]       port: 5001
[2026-03-26 20:23:13] [FRONTEND]     },
[2026-03-26 20:23:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:23:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:23:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:23:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:23:13] [FRONTEND]       errno: -61,
[2026-03-26 20:23:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:23:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:23:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:23:13] [FRONTEND]       port: 5001
[2026-03-26 20:23:13] [FRONTEND]     }
[2026-03-26 20:23:13] [FRONTEND]   ]
[2026-03-26 20:23:13] [FRONTEND] }
[2026-03-26 20:23:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:23:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:23:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:23:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:23:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:23:13] [FRONTEND]   [errors]: [
[2026-03-26 20:23:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:23:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:23:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:23:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:23:13] [FRONTEND]       errno: -61,
[2026-03-26 20:23:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:23:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:23:13] [FRONTEND]       address: '::1',
[2026-03-26 20:23:13] [FRONTEND]       port: 5001
[2026-03-26 20:23:13] [FRONTEND]     },
[2026-03-26 20:23:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:23:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:23:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:23:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:23:13] [FRONTEND]       errno: -61,
[2026-03-26 20:23:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:23:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:23:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:23:13] [FRONTEND]       port: 5001
[2026-03-26 20:23:13] [FRONTEND]     }
[2026-03-26 20:23:13] [FRONTEND]   ]
[2026-03-26 20:23:13] [FRONTEND] }
[2026-03-26 20:24:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:24:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:24:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:24:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:24:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:24:13] [FRONTEND]   [errors]: [
[2026-03-26 20:24:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:24:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:24:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:24:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:24:13] [FRONTEND]       errno: -61,
[2026-03-26 20:24:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:24:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:24:13] [FRONTEND]       address: '::1',
[2026-03-26 20:24:13] [FRONTEND]       port: 5001
[2026-03-26 20:24:13] [FRONTEND]     },
[2026-03-26 20:24:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:24:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:24:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:24:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:24:13] [FRONTEND]       errno: -61,
[2026-03-26 20:24:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:24:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:24:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:24:13] [FRONTEND]       port: 5001
[2026-03-26 20:24:13] [FRONTEND]     }
[2026-03-26 20:24:13] [FRONTEND]   ]
[2026-03-26 20:24:13] [FRONTEND] }
[2026-03-26 20:24:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:24:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:24:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:24:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:24:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:24:13] [FRONTEND]   [errors]: [
[2026-03-26 20:24:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:24:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:24:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:24:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:24:13] [FRONTEND]       errno: -61,
[2026-03-26 20:24:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:24:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:24:13] [FRONTEND]       address: '::1',
[2026-03-26 20:24:13] [FRONTEND]       port: 5001
[2026-03-26 20:24:13] [FRONTEND]     },
[2026-03-26 20:24:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:24:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:24:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:24:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:24:13] [FRONTEND]       errno: -61,
[2026-03-26 20:24:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:24:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:24:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:24:13] [FRONTEND]       port: 5001
[2026-03-26 20:24:13] [FRONTEND]     }
[2026-03-26 20:24:13] [FRONTEND]   ]
[2026-03-26 20:24:13] [FRONTEND] }
[2026-03-26 20:25:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:25:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:25:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:25:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:25:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:25:13] [FRONTEND]   [errors]: [
[2026-03-26 20:25:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:25:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:25:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:25:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:25:13] [FRONTEND]       errno: -61,
[2026-03-26 20:25:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:25:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:25:13] [FRONTEND]       address: '::1',
[2026-03-26 20:25:13] [FRONTEND]       port: 5001
[2026-03-26 20:25:13] [FRONTEND]     },
[2026-03-26 20:25:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:25:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:25:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:25:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:25:13] [FRONTEND]       errno: -61,
[2026-03-26 20:25:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:25:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:25:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:25:13] [FRONTEND]       port: 5001
[2026-03-26 20:25:13] [FRONTEND]     }
[2026-03-26 20:25:13] [FRONTEND]   ]
[2026-03-26 20:25:13] [FRONTEND] }
[2026-03-26 20:25:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:25:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:25:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:25:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:25:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:25:13] [FRONTEND]   [errors]: [
[2026-03-26 20:25:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:25:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:25:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:25:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:25:13] [FRONTEND]       errno: -61,
[2026-03-26 20:25:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:25:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:25:13] [FRONTEND]       address: '::1',
[2026-03-26 20:25:13] [FRONTEND]       port: 5001
[2026-03-26 20:25:13] [FRONTEND]     },
[2026-03-26 20:25:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:25:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:25:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:25:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:25:13] [FRONTEND]       errno: -61,
[2026-03-26 20:25:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:25:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:25:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:25:13] [FRONTEND]       port: 5001
[2026-03-26 20:25:13] [FRONTEND]     }
[2026-03-26 20:25:13] [FRONTEND]   ]
[2026-03-26 20:25:13] [FRONTEND] }
[2026-03-26 20:26:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:26:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:26:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:26:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:26:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:26:13] [FRONTEND]   [errors]: [
[2026-03-26 20:26:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:26:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:26:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:26:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:26:13] [FRONTEND]       errno: -61,
[2026-03-26 20:26:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:26:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:26:13] [FRONTEND]       address: '::1',
[2026-03-26 20:26:13] [FRONTEND]       port: 5001
[2026-03-26 20:26:13] [FRONTEND]     },
[2026-03-26 20:26:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:26:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:26:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:26:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:26:13] [FRONTEND]       errno: -61,
[2026-03-26 20:26:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:26:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:26:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:26:13] [FRONTEND]       port: 5001
[2026-03-26 20:26:13] [FRONTEND]     }
[2026-03-26 20:26:13] [FRONTEND]   ]
[2026-03-26 20:26:13] [FRONTEND] }
[2026-03-26 20:26:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:26:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:26:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:26:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:26:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:26:13] [FRONTEND]   [errors]: [
[2026-03-26 20:26:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:26:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:26:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:26:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:26:13] [FRONTEND]       errno: -61,
[2026-03-26 20:26:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:26:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:26:13] [FRONTEND]       address: '::1',
[2026-03-26 20:26:13] [FRONTEND]       port: 5001
[2026-03-26 20:26:13] [FRONTEND]     },
[2026-03-26 20:26:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:26:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:26:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:26:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:26:13] [FRONTEND]       errno: -61,
[2026-03-26 20:26:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:26:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:26:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:26:13] [FRONTEND]       port: 5001
[2026-03-26 20:26:13] [FRONTEND]     }
[2026-03-26 20:26:13] [FRONTEND]   ]
[2026-03-26 20:26:13] [FRONTEND] }
[2026-03-26 20:27:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:27:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:27:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:27:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:27:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:27:13] [FRONTEND]   [errors]: [
[2026-03-26 20:27:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:27:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:27:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:27:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:27:13] [FRONTEND]       errno: -61,
[2026-03-26 20:27:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:27:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:27:13] [FRONTEND]       address: '::1',
[2026-03-26 20:27:13] [FRONTEND]       port: 5001
[2026-03-26 20:27:13] [FRONTEND]     },
[2026-03-26 20:27:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:27:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:27:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:27:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:27:13] [FRONTEND]       errno: -61,
[2026-03-26 20:27:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:27:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:27:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:27:13] [FRONTEND]       port: 5001
[2026-03-26 20:27:13] [FRONTEND]     }
[2026-03-26 20:27:13] [FRONTEND]   ]
[2026-03-26 20:27:13] [FRONTEND] }
[2026-03-26 20:27:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:27:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:27:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:27:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:27:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:27:13] [FRONTEND]   [errors]: [
[2026-03-26 20:27:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:27:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:27:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:27:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:27:13] [FRONTEND]       errno: -61,
[2026-03-26 20:27:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:27:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:27:13] [FRONTEND]       address: '::1',
[2026-03-26 20:27:13] [FRONTEND]       port: 5001
[2026-03-26 20:27:13] [FRONTEND]     },
[2026-03-26 20:27:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:27:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:27:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:27:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:27:13] [FRONTEND]       errno: -61,
[2026-03-26 20:27:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:27:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:27:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:27:13] [FRONTEND]       port: 5001
[2026-03-26 20:27:13] [FRONTEND]     }
[2026-03-26 20:27:13] [FRONTEND]   ]
[2026-03-26 20:27:13] [FRONTEND] }
[2026-03-26 20:28:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:28:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:28:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:28:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:28:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:28:13] [FRONTEND]   [errors]: [
[2026-03-26 20:28:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:28:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:28:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:28:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:28:13] [FRONTEND]       errno: -61,
[2026-03-26 20:28:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:28:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:28:13] [FRONTEND]       address: '::1',
[2026-03-26 20:28:13] [FRONTEND]       port: 5001
[2026-03-26 20:28:13] [FRONTEND]     },
[2026-03-26 20:28:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:28:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:28:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:28:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:28:13] [FRONTEND]       errno: -61,
[2026-03-26 20:28:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:28:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:28:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:28:13] [FRONTEND]       port: 5001
[2026-03-26 20:28:13] [FRONTEND]     }
[2026-03-26 20:28:13] [FRONTEND]   ]
[2026-03-26 20:28:13] [FRONTEND] }
[2026-03-26 20:28:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:28:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:28:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:28:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:28:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:28:13] [FRONTEND]   [errors]: [
[2026-03-26 20:28:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:28:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:28:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:28:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:28:13] [FRONTEND]       errno: -61,
[2026-03-26 20:28:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:28:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:28:13] [FRONTEND]       address: '::1',
[2026-03-26 20:28:13] [FRONTEND]       port: 5001
[2026-03-26 20:28:13] [FRONTEND]     },
[2026-03-26 20:28:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:28:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:28:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:28:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:28:13] [FRONTEND]       errno: -61,
[2026-03-26 20:28:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:28:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:28:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:28:13] [FRONTEND]       port: 5001
[2026-03-26 20:28:13] [FRONTEND]     }
[2026-03-26 20:28:13] [FRONTEND]   ]
[2026-03-26 20:28:13] [FRONTEND] }
[2026-03-26 20:29:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:29:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:29:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:29:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:29:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:29:13] [FRONTEND]   [errors]: [
[2026-03-26 20:29:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:29:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:29:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:29:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:29:13] [FRONTEND]       errno: -61,
[2026-03-26 20:29:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:29:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:29:13] [FRONTEND]       address: '::1',
[2026-03-26 20:29:13] [FRONTEND]       port: 5001
[2026-03-26 20:29:13] [FRONTEND]     },
[2026-03-26 20:29:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:29:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:29:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:29:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:29:13] [FRONTEND]       errno: -61,
[2026-03-26 20:29:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:29:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:29:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:29:13] [FRONTEND]       port: 5001
[2026-03-26 20:29:13] [FRONTEND]     }
[2026-03-26 20:29:13] [FRONTEND]   ]
[2026-03-26 20:29:13] [FRONTEND] }
[2026-03-26 20:29:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:29:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:29:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:29:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:29:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:29:13] [FRONTEND]   [errors]: [
[2026-03-26 20:29:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:29:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:29:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:29:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:29:13] [FRONTEND]       errno: -61,
[2026-03-26 20:29:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:29:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:29:13] [FRONTEND]       address: '::1',
[2026-03-26 20:29:13] [FRONTEND]       port: 5001
[2026-03-26 20:29:13] [FRONTEND]     },
[2026-03-26 20:29:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:29:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:29:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:29:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:29:13] [FRONTEND]       errno: -61,
[2026-03-26 20:29:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:29:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:29:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:29:13] [FRONTEND]       port: 5001
[2026-03-26 20:29:13] [FRONTEND]     }
[2026-03-26 20:29:13] [FRONTEND]   ]
[2026-03-26 20:29:13] [FRONTEND] }
[2026-03-26 20:30:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:30:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:30:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:30:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:30:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:30:13] [FRONTEND]   [errors]: [
[2026-03-26 20:30:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:30:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:30:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:30:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:30:13] [FRONTEND]       errno: -61,
[2026-03-26 20:30:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:30:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:30:13] [FRONTEND]       address: '::1',
[2026-03-26 20:30:13] [FRONTEND]       port: 5001
[2026-03-26 20:30:13] [FRONTEND]     },
[2026-03-26 20:30:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:30:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:30:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:30:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:30:13] [FRONTEND]       errno: -61,
[2026-03-26 20:30:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:30:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:30:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:30:13] [FRONTEND]       port: 5001
[2026-03-26 20:30:13] [FRONTEND]     }
[2026-03-26 20:30:13] [FRONTEND]   ]
[2026-03-26 20:30:13] [FRONTEND] }
[2026-03-26 20:30:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:30:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:30:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:30:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:30:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:30:13] [FRONTEND]   [errors]: [
[2026-03-26 20:30:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:30:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:30:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:30:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:30:13] [FRONTEND]       errno: -61,
[2026-03-26 20:30:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:30:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:30:13] [FRONTEND]       address: '::1',
[2026-03-26 20:30:13] [FRONTEND]       port: 5001
[2026-03-26 20:30:13] [FRONTEND]     },
[2026-03-26 20:30:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:30:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:30:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:30:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:30:13] [FRONTEND]       errno: -61,
[2026-03-26 20:30:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:30:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:30:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:30:13] [FRONTEND]       port: 5001
[2026-03-26 20:30:13] [FRONTEND]     }
[2026-03-26 20:30:13] [FRONTEND]   ]
[2026-03-26 20:30:13] [FRONTEND] }
[2026-03-26 20:31:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:31:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:31:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:31:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:31:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:31:13] [FRONTEND]   [errors]: [
[2026-03-26 20:31:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:31:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:31:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:31:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:31:13] [FRONTEND]       errno: -61,
[2026-03-26 20:31:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:31:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:31:13] [FRONTEND]       address: '::1',
[2026-03-26 20:31:13] [FRONTEND]       port: 5001
[2026-03-26 20:31:13] [FRONTEND]     },
[2026-03-26 20:31:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:31:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:31:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:31:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:31:13] [FRONTEND]       errno: -61,
[2026-03-26 20:31:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:31:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:31:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:31:13] [FRONTEND]       port: 5001
[2026-03-26 20:31:13] [FRONTEND]     }
[2026-03-26 20:31:13] [FRONTEND]   ]
[2026-03-26 20:31:13] [FRONTEND] }
[2026-03-26 20:31:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:31:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:31:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:31:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:31:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:31:13] [FRONTEND]   [errors]: [
[2026-03-26 20:31:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:31:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:31:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:31:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:31:13] [FRONTEND]       errno: -61,
[2026-03-26 20:31:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:31:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:31:13] [FRONTEND]       address: '::1',
[2026-03-26 20:31:13] [FRONTEND]       port: 5001
[2026-03-26 20:31:13] [FRONTEND]     },
[2026-03-26 20:31:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:31:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:31:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:31:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:31:13] [FRONTEND]       errno: -61,
[2026-03-26 20:31:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:31:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:31:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:31:13] [FRONTEND]       port: 5001
[2026-03-26 20:31:13] [FRONTEND]     }
[2026-03-26 20:31:13] [FRONTEND]   ]
[2026-03-26 20:31:13] [FRONTEND] }
[2026-03-26 20:32:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:32:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:32:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:32:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:32:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:32:13] [FRONTEND]   [errors]: [
[2026-03-26 20:32:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:32:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:32:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:32:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:32:13] [FRONTEND]       errno: -61,
[2026-03-26 20:32:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:32:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:32:13] [FRONTEND]       address: '::1',
[2026-03-26 20:32:13] [FRONTEND]       port: 5001
[2026-03-26 20:32:13] [FRONTEND]     },
[2026-03-26 20:32:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:32:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:32:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:32:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:32:13] [FRONTEND]       errno: -61,
[2026-03-26 20:32:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:32:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:32:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:32:13] [FRONTEND]       port: 5001
[2026-03-26 20:32:13] [FRONTEND]     }
[2026-03-26 20:32:13] [FRONTEND]   ]
[2026-03-26 20:32:13] [FRONTEND] }
[2026-03-26 20:32:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:32:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:32:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:32:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:32:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:32:13] [FRONTEND]   [errors]: [
[2026-03-26 20:32:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:32:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:32:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:32:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:32:13] [FRONTEND]       errno: -61,
[2026-03-26 20:32:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:32:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:32:13] [FRONTEND]       address: '::1',
[2026-03-26 20:32:13] [FRONTEND]       port: 5001
[2026-03-26 20:32:13] [FRONTEND]     },
[2026-03-26 20:32:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:32:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:32:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:32:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:32:13] [FRONTEND]       errno: -61,
[2026-03-26 20:32:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:32:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:32:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:32:13] [FRONTEND]       port: 5001
[2026-03-26 20:32:13] [FRONTEND]     }
[2026-03-26 20:32:13] [FRONTEND]   ]
[2026-03-26 20:32:13] [FRONTEND] }
[2026-03-26 20:33:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:33:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:33:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:33:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:33:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:33:13] [FRONTEND]   [errors]: [
[2026-03-26 20:33:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:33:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:33:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:33:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:33:13] [FRONTEND]       errno: -61,
[2026-03-26 20:33:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:33:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:33:13] [FRONTEND]       address: '::1',
[2026-03-26 20:33:13] [FRONTEND]       port: 5001
[2026-03-26 20:33:13] [FRONTEND]     },
[2026-03-26 20:33:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:33:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:33:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:33:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:33:13] [FRONTEND]       errno: -61,
[2026-03-26 20:33:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:33:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:33:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:33:13] [FRONTEND]       port: 5001
[2026-03-26 20:33:13] [FRONTEND]     }
[2026-03-26 20:33:13] [FRONTEND]   ]
[2026-03-26 20:33:13] [FRONTEND] }
[2026-03-26 20:33:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:33:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:33:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:33:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:33:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:33:13] [FRONTEND]   [errors]: [
[2026-03-26 20:33:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:33:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:33:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:33:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:33:13] [FRONTEND]       errno: -61,
[2026-03-26 20:33:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:33:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:33:13] [FRONTEND]       address: '::1',
[2026-03-26 20:33:13] [FRONTEND]       port: 5001
[2026-03-26 20:33:13] [FRONTEND]     },
[2026-03-26 20:33:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:33:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:33:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:33:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:33:13] [FRONTEND]       errno: -61,
[2026-03-26 20:33:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:33:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:33:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:33:13] [FRONTEND]       port: 5001
[2026-03-26 20:33:13] [FRONTEND]     }
[2026-03-26 20:33:13] [FRONTEND]   ]
[2026-03-26 20:33:13] [FRONTEND] }
[2026-03-26 20:34:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:34:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:34:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:34:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:34:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:34:13] [FRONTEND]   [errors]: [
[2026-03-26 20:34:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:34:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:34:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:34:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:34:13] [FRONTEND]       errno: -61,
[2026-03-26 20:34:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:34:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:34:13] [FRONTEND]       address: '::1',
[2026-03-26 20:34:13] [FRONTEND]       port: 5001
[2026-03-26 20:34:13] [FRONTEND]     },
[2026-03-26 20:34:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:34:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:34:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:34:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:34:13] [FRONTEND]       errno: -61,
[2026-03-26 20:34:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:34:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:34:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:34:13] [FRONTEND]       port: 5001
[2026-03-26 20:34:13] [FRONTEND]     }
[2026-03-26 20:34:13] [FRONTEND]   ]
[2026-03-26 20:34:13] [FRONTEND] }
[2026-03-26 20:34:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:34:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:34:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:34:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:34:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:34:13] [FRONTEND]   [errors]: [
[2026-03-26 20:34:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:34:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:34:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:34:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:34:13] [FRONTEND]       errno: -61,
[2026-03-26 20:34:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:34:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:34:13] [FRONTEND]       address: '::1',
[2026-03-26 20:34:13] [FRONTEND]       port: 5001
[2026-03-26 20:34:13] [FRONTEND]     },
[2026-03-26 20:34:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:34:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:34:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:34:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:34:13] [FRONTEND]       errno: -61,
[2026-03-26 20:34:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:34:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:34:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:34:13] [FRONTEND]       port: 5001
[2026-03-26 20:34:13] [FRONTEND]     }
[2026-03-26 20:34:13] [FRONTEND]   ]
[2026-03-26 20:34:13] [FRONTEND] }
[2026-03-26 20:35:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:35:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:35:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:35:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:35:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:35:13] [FRONTEND]   [errors]: [
[2026-03-26 20:35:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:35:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:35:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:35:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:35:13] [FRONTEND]       errno: -61,
[2026-03-26 20:35:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:35:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:35:13] [FRONTEND]       address: '::1',
[2026-03-26 20:35:13] [FRONTEND]       port: 5001
[2026-03-26 20:35:13] [FRONTEND]     },
[2026-03-26 20:35:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:35:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:35:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:35:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:35:13] [FRONTEND]       errno: -61,
[2026-03-26 20:35:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:35:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:35:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:35:13] [FRONTEND]       port: 5001
[2026-03-26 20:35:13] [FRONTEND]     }
[2026-03-26 20:35:13] [FRONTEND]   ]
[2026-03-26 20:35:13] [FRONTEND] }
[2026-03-26 20:35:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:35:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:35:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:35:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:35:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:35:13] [FRONTEND]   [errors]: [
[2026-03-26 20:35:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:35:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:35:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:35:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:35:13] [FRONTEND]       errno: -61,
[2026-03-26 20:35:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:35:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:35:13] [FRONTEND]       address: '::1',
[2026-03-26 20:35:13] [FRONTEND]       port: 5001
[2026-03-26 20:35:13] [FRONTEND]     },
[2026-03-26 20:35:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:35:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:35:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:35:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:35:13] [FRONTEND]       errno: -61,
[2026-03-26 20:35:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:35:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:35:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:35:13] [FRONTEND]       port: 5001
[2026-03-26 20:35:13] [FRONTEND]     }
[2026-03-26 20:35:13] [FRONTEND]   ]
[2026-03-26 20:35:13] [FRONTEND] }
[2026-03-26 20:36:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:36:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:36:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:36:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:36:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:36:13] [FRONTEND]   [errors]: [
[2026-03-26 20:36:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:36:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:36:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:36:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:36:13] [FRONTEND]       errno: -61,
[2026-03-26 20:36:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:36:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:36:13] [FRONTEND]       address: '::1',
[2026-03-26 20:36:13] [FRONTEND]       port: 5001
[2026-03-26 20:36:13] [FRONTEND]     },
[2026-03-26 20:36:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:36:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:36:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:36:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:36:13] [FRONTEND]       errno: -61,
[2026-03-26 20:36:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:36:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:36:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:36:13] [FRONTEND]       port: 5001
[2026-03-26 20:36:13] [FRONTEND]     }
[2026-03-26 20:36:13] [FRONTEND]   ]
[2026-03-26 20:36:13] [FRONTEND] }
[2026-03-26 20:36:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:36:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:36:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:36:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:36:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:36:13] [FRONTEND]   [errors]: [
[2026-03-26 20:36:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:36:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:36:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:36:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:36:13] [FRONTEND]       errno: -61,
[2026-03-26 20:36:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:36:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:36:13] [FRONTEND]       address: '::1',
[2026-03-26 20:36:13] [FRONTEND]       port: 5001
[2026-03-26 20:36:13] [FRONTEND]     },
[2026-03-26 20:36:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:36:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:36:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:36:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:36:13] [FRONTEND]       errno: -61,
[2026-03-26 20:36:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:36:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:36:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:36:13] [FRONTEND]       port: 5001
[2026-03-26 20:36:13] [FRONTEND]     }
[2026-03-26 20:36:13] [FRONTEND]   ]
[2026-03-26 20:36:13] [FRONTEND] }
[2026-03-26 20:37:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:37:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:37:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:37:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:37:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:37:13] [FRONTEND]   [errors]: [
[2026-03-26 20:37:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:37:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:37:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:37:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:37:13] [FRONTEND]       errno: -61,
[2026-03-26 20:37:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:37:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:37:13] [FRONTEND]       address: '::1',
[2026-03-26 20:37:13] [FRONTEND]       port: 5001
[2026-03-26 20:37:13] [FRONTEND]     },
[2026-03-26 20:37:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:37:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:37:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:37:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:37:13] [FRONTEND]       errno: -61,
[2026-03-26 20:37:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:37:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:37:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:37:13] [FRONTEND]       port: 5001
[2026-03-26 20:37:13] [FRONTEND]     }
[2026-03-26 20:37:13] [FRONTEND]   ]
[2026-03-26 20:37:13] [FRONTEND] }
[2026-03-26 20:37:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:37:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:37:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:37:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:37:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:37:13] [FRONTEND]   [errors]: [
[2026-03-26 20:37:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:37:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:37:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:37:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:37:13] [FRONTEND]       errno: -61,
[2026-03-26 20:37:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:37:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:37:13] [FRONTEND]       address: '::1',
[2026-03-26 20:37:13] [FRONTEND]       port: 5001
[2026-03-26 20:37:13] [FRONTEND]     },
[2026-03-26 20:37:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:37:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:37:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:37:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:37:13] [FRONTEND]       errno: -61,
[2026-03-26 20:37:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:37:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:37:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:37:13] [FRONTEND]       port: 5001
[2026-03-26 20:37:13] [FRONTEND]     }
[2026-03-26 20:37:13] [FRONTEND]   ]
[2026-03-26 20:37:13] [FRONTEND] }
[2026-03-26 20:38:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:38:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:38:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:38:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:38:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:38:13] [FRONTEND]   [errors]: [
[2026-03-26 20:38:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:38:13] [FRONTEND]       errno: -61,
[2026-03-26 20:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:38:13] [FRONTEND]       address: '::1',
[2026-03-26 20:38:13] [FRONTEND]       port: 5001
[2026-03-26 20:38:13] [FRONTEND]     },
[2026-03-26 20:38:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:38:13] [FRONTEND]       errno: -61,
[2026-03-26 20:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:38:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:38:13] [FRONTEND]       port: 5001
[2026-03-26 20:38:13] [FRONTEND]     }
[2026-03-26 20:38:13] [FRONTEND]   ]
[2026-03-26 20:38:13] [FRONTEND] }
[2026-03-26 20:38:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:38:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:38:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:38:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:38:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:38:13] [FRONTEND]   [errors]: [
[2026-03-26 20:38:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:38:13] [FRONTEND]       errno: -61,
[2026-03-26 20:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:38:13] [FRONTEND]       address: '::1',
[2026-03-26 20:38:13] [FRONTEND]       port: 5001
[2026-03-26 20:38:13] [FRONTEND]     },
[2026-03-26 20:38:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:38:13] [FRONTEND]       errno: -61,
[2026-03-26 20:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:38:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:38:13] [FRONTEND]       port: 5001
[2026-03-26 20:38:13] [FRONTEND]     }
[2026-03-26 20:38:13] [FRONTEND]   ]
[2026-03-26 20:38:13] [FRONTEND] }
[2026-03-26 20:39:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:39:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:39:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:39:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:39:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:39:13] [FRONTEND]   [errors]: [
[2026-03-26 20:39:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:39:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:39:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:39:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:39:13] [FRONTEND]       errno: -61,
[2026-03-26 20:39:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:39:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:39:13] [FRONTEND]       address: '::1',
[2026-03-26 20:39:13] [FRONTEND]       port: 5001
[2026-03-26 20:39:13] [FRONTEND]     },
[2026-03-26 20:39:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:39:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:39:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:39:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:39:13] [FRONTEND]       errno: -61,
[2026-03-26 20:39:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:39:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:39:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:39:13] [FRONTEND]       port: 5001
[2026-03-26 20:39:13] [FRONTEND]     }
[2026-03-26 20:39:13] [FRONTEND]   ]
[2026-03-26 20:39:13] [FRONTEND] }
[2026-03-26 20:39:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:39:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:39:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:39:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:39:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:39:13] [FRONTEND]   [errors]: [
[2026-03-26 20:39:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:39:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:39:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:39:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:39:13] [FRONTEND]       errno: -61,
[2026-03-26 20:39:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:39:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:39:13] [FRONTEND]       address: '::1',
[2026-03-26 20:39:13] [FRONTEND]       port: 5001
[2026-03-26 20:39:13] [FRONTEND]     },
[2026-03-26 20:39:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:39:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:39:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:39:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:39:13] [FRONTEND]       errno: -61,
[2026-03-26 20:39:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:39:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:39:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:39:13] [FRONTEND]       port: 5001
[2026-03-26 20:39:13] [FRONTEND]     }
[2026-03-26 20:39:13] [FRONTEND]   ]
[2026-03-26 20:39:13] [FRONTEND] }
[2026-03-26 20:40:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:40:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:40:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:40:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:40:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:40:13] [FRONTEND]   [errors]: [
[2026-03-26 20:40:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:40:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:40:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:40:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:40:13] [FRONTEND]       errno: -61,
[2026-03-26 20:40:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:40:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:40:13] [FRONTEND]       address: '::1',
[2026-03-26 20:40:13] [FRONTEND]       port: 5001
[2026-03-26 20:40:13] [FRONTEND]     },
[2026-03-26 20:40:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:40:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:40:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:40:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:40:13] [FRONTEND]       errno: -61,
[2026-03-26 20:40:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:40:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:40:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:40:13] [FRONTEND]       port: 5001
[2026-03-26 20:40:13] [FRONTEND]     }
[2026-03-26 20:40:13] [FRONTEND]   ]
[2026-03-26 20:40:13] [FRONTEND] }
[2026-03-26 20:40:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:40:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:40:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:40:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:40:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:40:13] [FRONTEND]   [errors]: [
[2026-03-26 20:40:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:40:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:40:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:40:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:40:13] [FRONTEND]       errno: -61,
[2026-03-26 20:40:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:40:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:40:13] [FRONTEND]       address: '::1',
[2026-03-26 20:40:13] [FRONTEND]       port: 5001
[2026-03-26 20:40:13] [FRONTEND]     },
[2026-03-26 20:40:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:40:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:40:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:40:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:40:13] [FRONTEND]       errno: -61,
[2026-03-26 20:40:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:40:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:40:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:40:13] [FRONTEND]       port: 5001
[2026-03-26 20:40:13] [FRONTEND]     }
[2026-03-26 20:40:13] [FRONTEND]   ]
[2026-03-26 20:40:13] [FRONTEND] }
[2026-03-26 20:41:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:41:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:41:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:41:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:41:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:41:13] [FRONTEND]   [errors]: [
[2026-03-26 20:41:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:41:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:41:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:41:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:41:13] [FRONTEND]       errno: -61,
[2026-03-26 20:41:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:41:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:41:13] [FRONTEND]       address: '::1',
[2026-03-26 20:41:13] [FRONTEND]       port: 5001
[2026-03-26 20:41:13] [FRONTEND]     },
[2026-03-26 20:41:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:41:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:41:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:41:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:41:13] [FRONTEND]       errno: -61,
[2026-03-26 20:41:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:41:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:41:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:41:13] [FRONTEND]       port: 5001
[2026-03-26 20:41:13] [FRONTEND]     }
[2026-03-26 20:41:13] [FRONTEND]   ]
[2026-03-26 20:41:13] [FRONTEND] }
[2026-03-26 20:41:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:41:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:41:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:41:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:41:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:41:13] [FRONTEND]   [errors]: [
[2026-03-26 20:41:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:41:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:41:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:41:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:41:13] [FRONTEND]       errno: -61,
[2026-03-26 20:41:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:41:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:41:13] [FRONTEND]       address: '::1',
[2026-03-26 20:41:13] [FRONTEND]       port: 5001
[2026-03-26 20:41:13] [FRONTEND]     },
[2026-03-26 20:41:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:41:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:41:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:41:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:41:13] [FRONTEND]       errno: -61,
[2026-03-26 20:41:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:41:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:41:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:41:13] [FRONTEND]       port: 5001
[2026-03-26 20:41:13] [FRONTEND]     }
[2026-03-26 20:41:13] [FRONTEND]   ]
[2026-03-26 20:41:13] [FRONTEND] }
[2026-03-26 20:42:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:42:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:42:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:42:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:42:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:42:13] [FRONTEND]   [errors]: [
[2026-03-26 20:42:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:42:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:42:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:42:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:42:13] [FRONTEND]       errno: -61,
[2026-03-26 20:42:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:42:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:42:13] [FRONTEND]       address: '::1',
[2026-03-26 20:42:13] [FRONTEND]       port: 5001
[2026-03-26 20:42:13] [FRONTEND]     },
[2026-03-26 20:42:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:42:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:42:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:42:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:42:13] [FRONTEND]       errno: -61,
[2026-03-26 20:42:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:42:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:42:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:42:13] [FRONTEND]       port: 5001
[2026-03-26 20:42:13] [FRONTEND]     }
[2026-03-26 20:42:13] [FRONTEND]   ]
[2026-03-26 20:42:13] [FRONTEND] }
[2026-03-26 20:42:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:42:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:42:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:42:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:42:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:42:13] [FRONTEND]   [errors]: [
[2026-03-26 20:42:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:42:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:42:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:42:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:42:13] [FRONTEND]       errno: -61,
[2026-03-26 20:42:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:42:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:42:13] [FRONTEND]       address: '::1',
[2026-03-26 20:42:13] [FRONTEND]       port: 5001
[2026-03-26 20:42:13] [FRONTEND]     },
[2026-03-26 20:42:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:42:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:42:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:42:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:42:13] [FRONTEND]       errno: -61,
[2026-03-26 20:42:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:42:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:42:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:42:13] [FRONTEND]       port: 5001
[2026-03-26 20:42:13] [FRONTEND]     }
[2026-03-26 20:42:13] [FRONTEND]   ]
[2026-03-26 20:42:13] [FRONTEND] }
[2026-03-26 20:43:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:43:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:43:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:43:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:43:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:43:13] [FRONTEND]   [errors]: [
[2026-03-26 20:43:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:43:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:43:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:43:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:43:13] [FRONTEND]       errno: -61,
[2026-03-26 20:43:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:43:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:43:13] [FRONTEND]       address: '::1',
[2026-03-26 20:43:13] [FRONTEND]       port: 5001
[2026-03-26 20:43:13] [FRONTEND]     },
[2026-03-26 20:43:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:43:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:43:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:43:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:43:13] [FRONTEND]       errno: -61,
[2026-03-26 20:43:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:43:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:43:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:43:13] [FRONTEND]       port: 5001
[2026-03-26 20:43:13] [FRONTEND]     }
[2026-03-26 20:43:13] [FRONTEND]   ]
[2026-03-26 20:43:13] [FRONTEND] }
[2026-03-26 20:43:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:43:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:43:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:43:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:43:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:43:13] [FRONTEND]   [errors]: [
[2026-03-26 20:43:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:43:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:43:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:43:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:43:13] [FRONTEND]       errno: -61,
[2026-03-26 20:43:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:43:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:43:13] [FRONTEND]       address: '::1',
[2026-03-26 20:43:13] [FRONTEND]       port: 5001
[2026-03-26 20:43:13] [FRONTEND]     },
[2026-03-26 20:43:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:43:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:43:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:43:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:43:13] [FRONTEND]       errno: -61,
[2026-03-26 20:43:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:43:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:43:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:43:13] [FRONTEND]       port: 5001
[2026-03-26 20:43:13] [FRONTEND]     }
[2026-03-26 20:43:13] [FRONTEND]   ]
[2026-03-26 20:43:13] [FRONTEND] }
[2026-03-26 20:44:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:44:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:44:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:44:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:44:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:44:13] [FRONTEND]   [errors]: [
[2026-03-26 20:44:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:44:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:44:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:44:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:44:13] [FRONTEND]       errno: -61,
[2026-03-26 20:44:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:44:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:44:13] [FRONTEND]       address: '::1',
[2026-03-26 20:44:13] [FRONTEND]       port: 5001
[2026-03-26 20:44:13] [FRONTEND]     },
[2026-03-26 20:44:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:44:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:44:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:44:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:44:13] [FRONTEND]       errno: -61,
[2026-03-26 20:44:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:44:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:44:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:44:13] [FRONTEND]       port: 5001
[2026-03-26 20:44:13] [FRONTEND]     }
[2026-03-26 20:44:13] [FRONTEND]   ]
[2026-03-26 20:44:13] [FRONTEND] }
[2026-03-26 20:44:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:44:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:44:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:44:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:44:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:44:13] [FRONTEND]   [errors]: [
[2026-03-26 20:44:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:44:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:44:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:44:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:44:13] [FRONTEND]       errno: -61,
[2026-03-26 20:44:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:44:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:44:13] [FRONTEND]       address: '::1',
[2026-03-26 20:44:13] [FRONTEND]       port: 5001
[2026-03-26 20:44:13] [FRONTEND]     },
[2026-03-26 20:44:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:44:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:44:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:44:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:44:13] [FRONTEND]       errno: -61,
[2026-03-26 20:44:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:44:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:44:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:44:13] [FRONTEND]       port: 5001
[2026-03-26 20:44:13] [FRONTEND]     }
[2026-03-26 20:44:13] [FRONTEND]   ]
[2026-03-26 20:44:13] [FRONTEND] }
[2026-03-26 20:45:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:45:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:45:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:45:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:45:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:45:13] [FRONTEND]   [errors]: [
[2026-03-26 20:45:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:45:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:45:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:45:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:45:13] [FRONTEND]       errno: -61,
[2026-03-26 20:45:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:45:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:45:13] [FRONTEND]       address: '::1',
[2026-03-26 20:45:13] [FRONTEND]       port: 5001
[2026-03-26 20:45:13] [FRONTEND]     },
[2026-03-26 20:45:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:45:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:45:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:45:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:45:13] [FRONTEND]       errno: -61,
[2026-03-26 20:45:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:45:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:45:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:45:13] [FRONTEND]       port: 5001
[2026-03-26 20:45:13] [FRONTEND]     }
[2026-03-26 20:45:13] [FRONTEND]   ]
[2026-03-26 20:45:13] [FRONTEND] }
[2026-03-26 20:45:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:45:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:45:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:45:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:45:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:45:13] [FRONTEND]   [errors]: [
[2026-03-26 20:45:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:45:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:45:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:45:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:45:13] [FRONTEND]       errno: -61,
[2026-03-26 20:45:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:45:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:45:13] [FRONTEND]       address: '::1',
[2026-03-26 20:45:13] [FRONTEND]       port: 5001
[2026-03-26 20:45:13] [FRONTEND]     },
[2026-03-26 20:45:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:45:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:45:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:45:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:45:13] [FRONTEND]       errno: -61,
[2026-03-26 20:45:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:45:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:45:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:45:13] [FRONTEND]       port: 5001
[2026-03-26 20:45:13] [FRONTEND]     }
[2026-03-26 20:45:13] [FRONTEND]   ]
[2026-03-26 20:45:13] [FRONTEND] }
[2026-03-26 20:46:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:46:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:46:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:46:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:46:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:46:13] [FRONTEND]   [errors]: [
[2026-03-26 20:46:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:46:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:46:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:46:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:46:13] [FRONTEND]       errno: -61,
[2026-03-26 20:46:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:46:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:46:13] [FRONTEND]       address: '::1',
[2026-03-26 20:46:13] [FRONTEND]       port: 5001
[2026-03-26 20:46:13] [FRONTEND]     },
[2026-03-26 20:46:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:46:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:46:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:46:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:46:13] [FRONTEND]       errno: -61,
[2026-03-26 20:46:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:46:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:46:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:46:13] [FRONTEND]       port: 5001
[2026-03-26 20:46:13] [FRONTEND]     }
[2026-03-26 20:46:13] [FRONTEND]   ]
[2026-03-26 20:46:13] [FRONTEND] }
[2026-03-26 20:46:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:46:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:46:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:46:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:46:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:46:13] [FRONTEND]   [errors]: [
[2026-03-26 20:46:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:46:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:46:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:46:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:46:13] [FRONTEND]       errno: -61,
[2026-03-26 20:46:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:46:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:46:13] [FRONTEND]       address: '::1',
[2026-03-26 20:46:13] [FRONTEND]       port: 5001
[2026-03-26 20:46:13] [FRONTEND]     },
[2026-03-26 20:46:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:46:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:46:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:46:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:46:13] [FRONTEND]       errno: -61,
[2026-03-26 20:46:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:46:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:46:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:46:13] [FRONTEND]       port: 5001
[2026-03-26 20:46:13] [FRONTEND]     }
[2026-03-26 20:46:13] [FRONTEND]   ]
[2026-03-26 20:46:13] [FRONTEND] }
[2026-03-26 20:47:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:47:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:47:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:47:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:47:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:47:13] [FRONTEND]   [errors]: [
[2026-03-26 20:47:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:47:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:47:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:47:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:47:13] [FRONTEND]       errno: -61,
[2026-03-26 20:47:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:47:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:47:13] [FRONTEND]       address: '::1',
[2026-03-26 20:47:13] [FRONTEND]       port: 5001
[2026-03-26 20:47:13] [FRONTEND]     },
[2026-03-26 20:47:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:47:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:47:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:47:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:47:13] [FRONTEND]       errno: -61,
[2026-03-26 20:47:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:47:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:47:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:47:13] [FRONTEND]       port: 5001
[2026-03-26 20:47:13] [FRONTEND]     }
[2026-03-26 20:47:13] [FRONTEND]   ]
[2026-03-26 20:47:13] [FRONTEND] }
[2026-03-26 20:47:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:47:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:47:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:47:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:47:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:47:13] [FRONTEND]   [errors]: [
[2026-03-26 20:47:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:47:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:47:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:47:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:47:13] [FRONTEND]       errno: -61,
[2026-03-26 20:47:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:47:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:47:13] [FRONTEND]       address: '::1',
[2026-03-26 20:47:13] [FRONTEND]       port: 5001
[2026-03-26 20:47:13] [FRONTEND]     },
[2026-03-26 20:47:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:47:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:47:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:47:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:47:13] [FRONTEND]       errno: -61,
[2026-03-26 20:47:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:47:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:47:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:47:13] [FRONTEND]       port: 5001
[2026-03-26 20:47:13] [FRONTEND]     }
[2026-03-26 20:47:13] [FRONTEND]   ]
[2026-03-26 20:47:13] [FRONTEND] }
[2026-03-26 20:48:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:48:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:48:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:48:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:48:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:48:13] [FRONTEND]   [errors]: [
[2026-03-26 20:48:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:48:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:48:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:48:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:48:13] [FRONTEND]       errno: -61,
[2026-03-26 20:48:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:48:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:48:13] [FRONTEND]       address: '::1',
[2026-03-26 20:48:13] [FRONTEND]       port: 5001
[2026-03-26 20:48:13] [FRONTEND]     },
[2026-03-26 20:48:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:48:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:48:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:48:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:48:13] [FRONTEND]       errno: -61,
[2026-03-26 20:48:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:48:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:48:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:48:13] [FRONTEND]       port: 5001
[2026-03-26 20:48:13] [FRONTEND]     }
[2026-03-26 20:48:13] [FRONTEND]   ]
[2026-03-26 20:48:13] [FRONTEND] }
[2026-03-26 20:48:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:48:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:48:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:48:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:48:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:48:13] [FRONTEND]   [errors]: [
[2026-03-26 20:48:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:48:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:48:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:48:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:48:13] [FRONTEND]       errno: -61,
[2026-03-26 20:48:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:48:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:48:13] [FRONTEND]       address: '::1',
[2026-03-26 20:48:13] [FRONTEND]       port: 5001
[2026-03-26 20:48:13] [FRONTEND]     },
[2026-03-26 20:48:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:48:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:48:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:48:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:48:13] [FRONTEND]       errno: -61,
[2026-03-26 20:48:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:48:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:48:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:48:13] [FRONTEND]       port: 5001
[2026-03-26 20:48:13] [FRONTEND]     }
[2026-03-26 20:48:13] [FRONTEND]   ]
[2026-03-26 20:48:13] [FRONTEND] }
[2026-03-26 20:49:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:49:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:49:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:49:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:49:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:49:13] [FRONTEND]   [errors]: [
[2026-03-26 20:49:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:49:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:49:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:49:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:49:13] [FRONTEND]       errno: -61,
[2026-03-26 20:49:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:49:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:49:13] [FRONTEND]       address: '::1',
[2026-03-26 20:49:13] [FRONTEND]       port: 5001
[2026-03-26 20:49:13] [FRONTEND]     },
[2026-03-26 20:49:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:49:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:49:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:49:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:49:13] [FRONTEND]       errno: -61,
[2026-03-26 20:49:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:49:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:49:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:49:13] [FRONTEND]       port: 5001
[2026-03-26 20:49:13] [FRONTEND]     }
[2026-03-26 20:49:13] [FRONTEND]   ]
[2026-03-26 20:49:13] [FRONTEND] }
[2026-03-26 20:49:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:49:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:49:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:49:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:49:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:49:13] [FRONTEND]   [errors]: [
[2026-03-26 20:49:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:49:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:49:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:49:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:49:13] [FRONTEND]       errno: -61,
[2026-03-26 20:49:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:49:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:49:13] [FRONTEND]       address: '::1',
[2026-03-26 20:49:13] [FRONTEND]       port: 5001
[2026-03-26 20:49:13] [FRONTEND]     },
[2026-03-26 20:49:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:49:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:49:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:49:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:49:13] [FRONTEND]       errno: -61,
[2026-03-26 20:49:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:49:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:49:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:49:13] [FRONTEND]       port: 5001
[2026-03-26 20:49:13] [FRONTEND]     }
[2026-03-26 20:49:13] [FRONTEND]   ]
[2026-03-26 20:49:13] [FRONTEND] }
[2026-03-26 20:50:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:50:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:50:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:50:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:50:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:50:13] [FRONTEND]   [errors]: [
[2026-03-26 20:50:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:50:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:50:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:50:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:50:13] [FRONTEND]       errno: -61,
[2026-03-26 20:50:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:50:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:50:13] [FRONTEND]       address: '::1',
[2026-03-26 20:50:13] [FRONTEND]       port: 5001
[2026-03-26 20:50:13] [FRONTEND]     },
[2026-03-26 20:50:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:50:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:50:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:50:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:50:13] [FRONTEND]       errno: -61,
[2026-03-26 20:50:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:50:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:50:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:50:13] [FRONTEND]       port: 5001
[2026-03-26 20:50:13] [FRONTEND]     }
[2026-03-26 20:50:13] [FRONTEND]   ]
[2026-03-26 20:50:13] [FRONTEND] }
[2026-03-26 20:50:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:50:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:50:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:50:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:50:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:50:13] [FRONTEND]   [errors]: [
[2026-03-26 20:50:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:50:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:50:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:50:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:50:13] [FRONTEND]       errno: -61,
[2026-03-26 20:50:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:50:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:50:13] [FRONTEND]       address: '::1',
[2026-03-26 20:50:13] [FRONTEND]       port: 5001
[2026-03-26 20:50:13] [FRONTEND]     },
[2026-03-26 20:50:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:50:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:50:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:50:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:50:13] [FRONTEND]       errno: -61,
[2026-03-26 20:50:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:50:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:50:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:50:13] [FRONTEND]       port: 5001
[2026-03-26 20:50:13] [FRONTEND]     }
[2026-03-26 20:50:13] [FRONTEND]   ]
[2026-03-26 20:50:13] [FRONTEND] }
[2026-03-26 20:51:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:51:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:51:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:51:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:51:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:51:13] [FRONTEND]   [errors]: [
[2026-03-26 20:51:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:51:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:51:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:51:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:51:13] [FRONTEND]       errno: -61,
[2026-03-26 20:51:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:51:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:51:13] [FRONTEND]       address: '::1',
[2026-03-26 20:51:13] [FRONTEND]       port: 5001
[2026-03-26 20:51:13] [FRONTEND]     },
[2026-03-26 20:51:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:51:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:51:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:51:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:51:13] [FRONTEND]       errno: -61,
[2026-03-26 20:51:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:51:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:51:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:51:13] [FRONTEND]       port: 5001
[2026-03-26 20:51:13] [FRONTEND]     }
[2026-03-26 20:51:13] [FRONTEND]   ]
[2026-03-26 20:51:13] [FRONTEND] }
[2026-03-26 20:51:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:51:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:51:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:51:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:51:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:51:13] [FRONTEND]   [errors]: [
[2026-03-26 20:51:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:51:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:51:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:51:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:51:13] [FRONTEND]       errno: -61,
[2026-03-26 20:51:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:51:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:51:13] [FRONTEND]       address: '::1',
[2026-03-26 20:51:13] [FRONTEND]       port: 5001
[2026-03-26 20:51:13] [FRONTEND]     },
[2026-03-26 20:51:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:51:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:51:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:51:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:51:13] [FRONTEND]       errno: -61,
[2026-03-26 20:51:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:51:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:51:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:51:13] [FRONTEND]       port: 5001
[2026-03-26 20:51:13] [FRONTEND]     }
[2026-03-26 20:51:13] [FRONTEND]   ]
[2026-03-26 20:51:13] [FRONTEND] }
[2026-03-26 20:52:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:52:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:52:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:52:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:52:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:52:13] [FRONTEND]   [errors]: [
[2026-03-26 20:52:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:52:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:52:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:52:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:52:13] [FRONTEND]       errno: -61,
[2026-03-26 20:52:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:52:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:52:13] [FRONTEND]       address: '::1',
[2026-03-26 20:52:13] [FRONTEND]       port: 5001
[2026-03-26 20:52:13] [FRONTEND]     },
[2026-03-26 20:52:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:52:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:52:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:52:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:52:13] [FRONTEND]       errno: -61,
[2026-03-26 20:52:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:52:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:52:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:52:13] [FRONTEND]       port: 5001
[2026-03-26 20:52:13] [FRONTEND]     }
[2026-03-26 20:52:13] [FRONTEND]   ]
[2026-03-26 20:52:13] [FRONTEND] }
[2026-03-26 20:52:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:52:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:52:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:52:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:52:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:52:13] [FRONTEND]   [errors]: [
[2026-03-26 20:52:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:52:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:52:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:52:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:52:13] [FRONTEND]       errno: -61,
[2026-03-26 20:52:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:52:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:52:13] [FRONTEND]       address: '::1',
[2026-03-26 20:52:13] [FRONTEND]       port: 5001
[2026-03-26 20:52:13] [FRONTEND]     },
[2026-03-26 20:52:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:52:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:52:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:52:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:52:13] [FRONTEND]       errno: -61,
[2026-03-26 20:52:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:52:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:52:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:52:13] [FRONTEND]       port: 5001
[2026-03-26 20:52:13] [FRONTEND]     }
[2026-03-26 20:52:13] [FRONTEND]   ]
[2026-03-26 20:52:13] [FRONTEND] }
[2026-03-26 20:53:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:53:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:53:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:53:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:53:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:53:13] [FRONTEND]   [errors]: [
[2026-03-26 20:53:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:53:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:53:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:53:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:53:13] [FRONTEND]       errno: -61,
[2026-03-26 20:53:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:53:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:53:13] [FRONTEND]       address: '::1',
[2026-03-26 20:53:13] [FRONTEND]       port: 5001
[2026-03-26 20:53:13] [FRONTEND]     },
[2026-03-26 20:53:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:53:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:53:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:53:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:53:13] [FRONTEND]       errno: -61,
[2026-03-26 20:53:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:53:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:53:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:53:13] [FRONTEND]       port: 5001
[2026-03-26 20:53:13] [FRONTEND]     }
[2026-03-26 20:53:13] [FRONTEND]   ]
[2026-03-26 20:53:13] [FRONTEND] }
[2026-03-26 20:53:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:53:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:53:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:53:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:53:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:53:13] [FRONTEND]   [errors]: [
[2026-03-26 20:53:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:53:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:53:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:53:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:53:13] [FRONTEND]       errno: -61,
[2026-03-26 20:53:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:53:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:53:13] [FRONTEND]       address: '::1',
[2026-03-26 20:53:13] [FRONTEND]       port: 5001
[2026-03-26 20:53:13] [FRONTEND]     },
[2026-03-26 20:53:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:53:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:53:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:53:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:53:13] [FRONTEND]       errno: -61,
[2026-03-26 20:53:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:53:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:53:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:53:13] [FRONTEND]       port: 5001
[2026-03-26 20:53:13] [FRONTEND]     }
[2026-03-26 20:53:13] [FRONTEND]   ]
[2026-03-26 20:53:13] [FRONTEND] }
[2026-03-26 20:54:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:54:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:54:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:54:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:54:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:54:13] [FRONTEND]   [errors]: [
[2026-03-26 20:54:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:54:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:54:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:54:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:54:13] [FRONTEND]       errno: -61,
[2026-03-26 20:54:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:54:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:54:13] [FRONTEND]       address: '::1',
[2026-03-26 20:54:13] [FRONTEND]       port: 5001
[2026-03-26 20:54:13] [FRONTEND]     },
[2026-03-26 20:54:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:54:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:54:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:54:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:54:13] [FRONTEND]       errno: -61,
[2026-03-26 20:54:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:54:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:54:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:54:13] [FRONTEND]       port: 5001
[2026-03-26 20:54:13] [FRONTEND]     }
[2026-03-26 20:54:13] [FRONTEND]   ]
[2026-03-26 20:54:13] [FRONTEND] }
[2026-03-26 20:54:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:54:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:54:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:54:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:54:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:54:13] [FRONTEND]   [errors]: [
[2026-03-26 20:54:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:54:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:54:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:54:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:54:13] [FRONTEND]       errno: -61,
[2026-03-26 20:54:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:54:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:54:13] [FRONTEND]       address: '::1',
[2026-03-26 20:54:13] [FRONTEND]       port: 5001
[2026-03-26 20:54:13] [FRONTEND]     },
[2026-03-26 20:54:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:54:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:54:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:54:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:54:13] [FRONTEND]       errno: -61,
[2026-03-26 20:54:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:54:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:54:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:54:13] [FRONTEND]       port: 5001
[2026-03-26 20:54:13] [FRONTEND]     }
[2026-03-26 20:54:13] [FRONTEND]   ]
[2026-03-26 20:54:13] [FRONTEND] }
[2026-03-26 20:55:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:55:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:55:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:55:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:55:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:55:13] [FRONTEND]   [errors]: [
[2026-03-26 20:55:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:55:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:55:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:55:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:55:13] [FRONTEND]       errno: -61,
[2026-03-26 20:55:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:55:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:55:13] [FRONTEND]       address: '::1',
[2026-03-26 20:55:13] [FRONTEND]       port: 5001
[2026-03-26 20:55:13] [FRONTEND]     },
[2026-03-26 20:55:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:55:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:55:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:55:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:55:13] [FRONTEND]       errno: -61,
[2026-03-26 20:55:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:55:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:55:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:55:13] [FRONTEND]       port: 5001
[2026-03-26 20:55:13] [FRONTEND]     }
[2026-03-26 20:55:13] [FRONTEND]   ]
[2026-03-26 20:55:13] [FRONTEND] }
[2026-03-26 20:55:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:55:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:55:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:55:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:55:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:55:13] [FRONTEND]   [errors]: [
[2026-03-26 20:55:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:55:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:55:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:55:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:55:13] [FRONTEND]       errno: -61,
[2026-03-26 20:55:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:55:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:55:13] [FRONTEND]       address: '::1',
[2026-03-26 20:55:13] [FRONTEND]       port: 5001
[2026-03-26 20:55:13] [FRONTEND]     },
[2026-03-26 20:55:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:55:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:55:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:55:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:55:13] [FRONTEND]       errno: -61,
[2026-03-26 20:55:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:55:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:55:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:55:13] [FRONTEND]       port: 5001
[2026-03-26 20:55:13] [FRONTEND]     }
[2026-03-26 20:55:13] [FRONTEND]   ]
[2026-03-26 20:55:13] [FRONTEND] }
[2026-03-26 20:56:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:56:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:56:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:56:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:56:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:56:13] [FRONTEND]   [errors]: [
[2026-03-26 20:56:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:56:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:56:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:56:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:56:13] [FRONTEND]       errno: -61,
[2026-03-26 20:56:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:56:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:56:13] [FRONTEND]       address: '::1',
[2026-03-26 20:56:13] [FRONTEND]       port: 5001
[2026-03-26 20:56:13] [FRONTEND]     },
[2026-03-26 20:56:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:56:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:56:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:56:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:56:13] [FRONTEND]       errno: -61,
[2026-03-26 20:56:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:56:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:56:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:56:13] [FRONTEND]       port: 5001
[2026-03-26 20:56:13] [FRONTEND]     }
[2026-03-26 20:56:13] [FRONTEND]   ]
[2026-03-26 20:56:13] [FRONTEND] }
[2026-03-26 20:56:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:56:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:56:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:56:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:56:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:56:13] [FRONTEND]   [errors]: [
[2026-03-26 20:56:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:56:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:56:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:56:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:56:13] [FRONTEND]       errno: -61,
[2026-03-26 20:56:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:56:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:56:13] [FRONTEND]       address: '::1',
[2026-03-26 20:56:13] [FRONTEND]       port: 5001
[2026-03-26 20:56:13] [FRONTEND]     },
[2026-03-26 20:56:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:56:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:56:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:56:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:56:13] [FRONTEND]       errno: -61,
[2026-03-26 20:56:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:56:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:56:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:56:13] [FRONTEND]       port: 5001
[2026-03-26 20:56:13] [FRONTEND]     }
[2026-03-26 20:56:13] [FRONTEND]   ]
[2026-03-26 20:56:13] [FRONTEND] }
[2026-03-26 20:57:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:57:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:57:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:57:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:57:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:57:13] [FRONTEND]   [errors]: [
[2026-03-26 20:57:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:57:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:57:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:57:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:57:13] [FRONTEND]       errno: -61,
[2026-03-26 20:57:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:57:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:57:13] [FRONTEND]       address: '::1',
[2026-03-26 20:57:13] [FRONTEND]       port: 5001
[2026-03-26 20:57:13] [FRONTEND]     },
[2026-03-26 20:57:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:57:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:57:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:57:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:57:13] [FRONTEND]       errno: -61,
[2026-03-26 20:57:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:57:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:57:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:57:13] [FRONTEND]       port: 5001
[2026-03-26 20:57:13] [FRONTEND]     }
[2026-03-26 20:57:13] [FRONTEND]   ]
[2026-03-26 20:57:13] [FRONTEND] }
[2026-03-26 20:57:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:57:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:57:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:57:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:57:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:57:13] [FRONTEND]   [errors]: [
[2026-03-26 20:57:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:57:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:57:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:57:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:57:13] [FRONTEND]       errno: -61,
[2026-03-26 20:57:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:57:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:57:13] [FRONTEND]       address: '::1',
[2026-03-26 20:57:13] [FRONTEND]       port: 5001
[2026-03-26 20:57:13] [FRONTEND]     },
[2026-03-26 20:57:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:57:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:57:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:57:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:57:13] [FRONTEND]       errno: -61,
[2026-03-26 20:57:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:57:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:57:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:57:13] [FRONTEND]       port: 5001
[2026-03-26 20:57:13] [FRONTEND]     }
[2026-03-26 20:57:13] [FRONTEND]   ]
[2026-03-26 20:57:13] [FRONTEND] }
[2026-03-26 20:58:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:58:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:58:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:58:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:58:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:58:13] [FRONTEND]   [errors]: [
[2026-03-26 20:58:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:58:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:58:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:58:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:58:13] [FRONTEND]       errno: -61,
[2026-03-26 20:58:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:58:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:58:13] [FRONTEND]       address: '::1',
[2026-03-26 20:58:13] [FRONTEND]       port: 5001
[2026-03-26 20:58:13] [FRONTEND]     },
[2026-03-26 20:58:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:58:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:58:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:58:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:58:13] [FRONTEND]       errno: -61,
[2026-03-26 20:58:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:58:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:58:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:58:13] [FRONTEND]       port: 5001
[2026-03-26 20:58:13] [FRONTEND]     }
[2026-03-26 20:58:13] [FRONTEND]   ]
[2026-03-26 20:58:13] [FRONTEND] }
[2026-03-26 20:58:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:58:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:58:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:58:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:58:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:58:13] [FRONTEND]   [errors]: [
[2026-03-26 20:58:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:58:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:58:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:58:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:58:13] [FRONTEND]       errno: -61,
[2026-03-26 20:58:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:58:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:58:13] [FRONTEND]       address: '::1',
[2026-03-26 20:58:13] [FRONTEND]       port: 5001
[2026-03-26 20:58:13] [FRONTEND]     },
[2026-03-26 20:58:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:58:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:58:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:58:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:58:13] [FRONTEND]       errno: -61,
[2026-03-26 20:58:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:58:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:58:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:58:13] [FRONTEND]       port: 5001
[2026-03-26 20:58:13] [FRONTEND]     }
[2026-03-26 20:58:13] [FRONTEND]   ]
[2026-03-26 20:58:13] [FRONTEND] }
[2026-03-26 20:59:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 20:59:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:59:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:59:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:59:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:59:13] [FRONTEND]   [errors]: [
[2026-03-26 20:59:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:59:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:59:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:59:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:59:13] [FRONTEND]       errno: -61,
[2026-03-26 20:59:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:59:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:59:13] [FRONTEND]       address: '::1',
[2026-03-26 20:59:13] [FRONTEND]       port: 5001
[2026-03-26 20:59:13] [FRONTEND]     },
[2026-03-26 20:59:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:59:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:59:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:59:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:59:13] [FRONTEND]       errno: -61,
[2026-03-26 20:59:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:59:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:59:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:59:13] [FRONTEND]       port: 5001
[2026-03-26 20:59:13] [FRONTEND]     }
[2026-03-26 20:59:13] [FRONTEND]   ]
[2026-03-26 20:59:13] [FRONTEND] }
[2026-03-26 20:59:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 20:59:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 20:59:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 20:59:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:59:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 20:59:13] [FRONTEND]   [errors]: [
[2026-03-26 20:59:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 20:59:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:59:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:59:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:59:13] [FRONTEND]       errno: -61,
[2026-03-26 20:59:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:59:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:59:13] [FRONTEND]       address: '::1',
[2026-03-26 20:59:13] [FRONTEND]       port: 5001
[2026-03-26 20:59:13] [FRONTEND]     },
[2026-03-26 20:59:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 20:59:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 20:59:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 20:59:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 20:59:13] [FRONTEND]       errno: -61,
[2026-03-26 20:59:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 20:59:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 20:59:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 20:59:13] [FRONTEND]       port: 5001
[2026-03-26 20:59:13] [FRONTEND]     }
[2026-03-26 20:59:13] [FRONTEND]   ]
[2026-03-26 20:59:13] [FRONTEND] }
[2026-03-26 21:00:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:00:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:00:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:00:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:00:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:00:13] [FRONTEND]   [errors]: [
[2026-03-26 21:00:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:00:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:00:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:00:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:00:13] [FRONTEND]       errno: -61,
[2026-03-26 21:00:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:00:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:00:13] [FRONTEND]       address: '::1',
[2026-03-26 21:00:13] [FRONTEND]       port: 5001
[2026-03-26 21:00:13] [FRONTEND]     },
[2026-03-26 21:00:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:00:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:00:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:00:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:00:13] [FRONTEND]       errno: -61,
[2026-03-26 21:00:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:00:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:00:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:00:13] [FRONTEND]       port: 5001
[2026-03-26 21:00:13] [FRONTEND]     }
[2026-03-26 21:00:13] [FRONTEND]   ]
[2026-03-26 21:00:13] [FRONTEND] }
[2026-03-26 21:00:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:00:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:00:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:00:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:00:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:00:13] [FRONTEND]   [errors]: [
[2026-03-26 21:00:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:00:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:00:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:00:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:00:13] [FRONTEND]       errno: -61,
[2026-03-26 21:00:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:00:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:00:13] [FRONTEND]       address: '::1',
[2026-03-26 21:00:13] [FRONTEND]       port: 5001
[2026-03-26 21:00:13] [FRONTEND]     },
[2026-03-26 21:00:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:00:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:00:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:00:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:00:13] [FRONTEND]       errno: -61,
[2026-03-26 21:00:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:00:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:00:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:00:13] [FRONTEND]       port: 5001
[2026-03-26 21:00:13] [FRONTEND]     }
[2026-03-26 21:00:13] [FRONTEND]   ]
[2026-03-26 21:00:13] [FRONTEND] }
[2026-03-26 21:01:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:01:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:01:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:01:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:01:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:01:13] [FRONTEND]   [errors]: [
[2026-03-26 21:01:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:01:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:01:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:01:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:01:13] [FRONTEND]       errno: -61,
[2026-03-26 21:01:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:01:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:01:13] [FRONTEND]       address: '::1',
[2026-03-26 21:01:13] [FRONTEND]       port: 5001
[2026-03-26 21:01:13] [FRONTEND]     },
[2026-03-26 21:01:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:01:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:01:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:01:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:01:13] [FRONTEND]       errno: -61,
[2026-03-26 21:01:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:01:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:01:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:01:13] [FRONTEND]       port: 5001
[2026-03-26 21:01:13] [FRONTEND]     }
[2026-03-26 21:01:13] [FRONTEND]   ]
[2026-03-26 21:01:13] [FRONTEND] }
[2026-03-26 21:01:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:01:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:01:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:01:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:01:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:01:13] [FRONTEND]   [errors]: [
[2026-03-26 21:01:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:01:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:01:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:01:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:01:13] [FRONTEND]       errno: -61,
[2026-03-26 21:01:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:01:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:01:13] [FRONTEND]       address: '::1',
[2026-03-26 21:01:13] [FRONTEND]       port: 5001
[2026-03-26 21:01:13] [FRONTEND]     },
[2026-03-26 21:01:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:01:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:01:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:01:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:01:13] [FRONTEND]       errno: -61,
[2026-03-26 21:01:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:01:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:01:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:01:13] [FRONTEND]       port: 5001
[2026-03-26 21:01:13] [FRONTEND]     }
[2026-03-26 21:01:13] [FRONTEND]   ]
[2026-03-26 21:01:13] [FRONTEND] }
[2026-03-26 21:02:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:02:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:02:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:02:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:02:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:02:13] [FRONTEND]   [errors]: [
[2026-03-26 21:02:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:02:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:02:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:02:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:02:13] [FRONTEND]       errno: -61,
[2026-03-26 21:02:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:02:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:02:13] [FRONTEND]       address: '::1',
[2026-03-26 21:02:13] [FRONTEND]       port: 5001
[2026-03-26 21:02:13] [FRONTEND]     },
[2026-03-26 21:02:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:02:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:02:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:02:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:02:13] [FRONTEND]       errno: -61,
[2026-03-26 21:02:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:02:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:02:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:02:13] [FRONTEND]       port: 5001
[2026-03-26 21:02:13] [FRONTEND]     }
[2026-03-26 21:02:13] [FRONTEND]   ]
[2026-03-26 21:02:13] [FRONTEND] }
[2026-03-26 21:02:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:02:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:02:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:02:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:02:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:02:13] [FRONTEND]   [errors]: [
[2026-03-26 21:02:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:02:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:02:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:02:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:02:13] [FRONTEND]       errno: -61,
[2026-03-26 21:02:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:02:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:02:13] [FRONTEND]       address: '::1',
[2026-03-26 21:02:13] [FRONTEND]       port: 5001
[2026-03-26 21:02:13] [FRONTEND]     },
[2026-03-26 21:02:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:02:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:02:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:02:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:02:13] [FRONTEND]       errno: -61,
[2026-03-26 21:02:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:02:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:02:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:02:13] [FRONTEND]       port: 5001
[2026-03-26 21:02:13] [FRONTEND]     }
[2026-03-26 21:02:13] [FRONTEND]   ]
[2026-03-26 21:02:13] [FRONTEND] }
[2026-03-26 21:03:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:03:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:03:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:03:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:03:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:03:13] [FRONTEND]   [errors]: [
[2026-03-26 21:03:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:03:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:03:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:03:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:03:13] [FRONTEND]       errno: -61,
[2026-03-26 21:03:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:03:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:03:13] [FRONTEND]       address: '::1',
[2026-03-26 21:03:13] [FRONTEND]       port: 5001
[2026-03-26 21:03:13] [FRONTEND]     },
[2026-03-26 21:03:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:03:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:03:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:03:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:03:13] [FRONTEND]       errno: -61,
[2026-03-26 21:03:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:03:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:03:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:03:13] [FRONTEND]       port: 5001
[2026-03-26 21:03:13] [FRONTEND]     }
[2026-03-26 21:03:13] [FRONTEND]   ]
[2026-03-26 21:03:13] [FRONTEND] }
[2026-03-26 21:03:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:03:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:03:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:03:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:03:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:03:13] [FRONTEND]   [errors]: [
[2026-03-26 21:03:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:03:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:03:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:03:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:03:13] [FRONTEND]       errno: -61,
[2026-03-26 21:03:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:03:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:03:13] [FRONTEND]       address: '::1',
[2026-03-26 21:03:13] [FRONTEND]       port: 5001
[2026-03-26 21:03:13] [FRONTEND]     },
[2026-03-26 21:03:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:03:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:03:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:03:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:03:13] [FRONTEND]       errno: -61,
[2026-03-26 21:03:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:03:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:03:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:03:13] [FRONTEND]       port: 5001
[2026-03-26 21:03:13] [FRONTEND]     }
[2026-03-26 21:03:13] [FRONTEND]   ]
[2026-03-26 21:03:13] [FRONTEND] }
[2026-03-26 21:04:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:04:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:04:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:04:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:04:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:04:13] [FRONTEND]   [errors]: [
[2026-03-26 21:04:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:04:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:04:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:04:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:04:13] [FRONTEND]       errno: -61,
[2026-03-26 21:04:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:04:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:04:13] [FRONTEND]       address: '::1',
[2026-03-26 21:04:13] [FRONTEND]       port: 5001
[2026-03-26 21:04:13] [FRONTEND]     },
[2026-03-26 21:04:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:04:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:04:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:04:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:04:13] [FRONTEND]       errno: -61,
[2026-03-26 21:04:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:04:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:04:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:04:13] [FRONTEND]       port: 5001
[2026-03-26 21:04:13] [FRONTEND]     }
[2026-03-26 21:04:13] [FRONTEND]   ]
[2026-03-26 21:04:13] [FRONTEND] }
[2026-03-26 21:04:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:04:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:04:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:04:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:04:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:04:13] [FRONTEND]   [errors]: [
[2026-03-26 21:04:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:04:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:04:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:04:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:04:13] [FRONTEND]       errno: -61,
[2026-03-26 21:04:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:04:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:04:13] [FRONTEND]       address: '::1',
[2026-03-26 21:04:13] [FRONTEND]       port: 5001
[2026-03-26 21:04:13] [FRONTEND]     },
[2026-03-26 21:04:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:04:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:04:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:04:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:04:13] [FRONTEND]       errno: -61,
[2026-03-26 21:04:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:04:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:04:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:04:13] [FRONTEND]       port: 5001
[2026-03-26 21:04:13] [FRONTEND]     }
[2026-03-26 21:04:13] [FRONTEND]   ]
[2026-03-26 21:04:13] [FRONTEND] }
[2026-03-26 21:05:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:05:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:05:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:05:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:05:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:05:13] [FRONTEND]   [errors]: [
[2026-03-26 21:05:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:05:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:05:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:05:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:05:13] [FRONTEND]       errno: -61,
[2026-03-26 21:05:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:05:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:05:13] [FRONTEND]       address: '::1',
[2026-03-26 21:05:13] [FRONTEND]       port: 5001
[2026-03-26 21:05:13] [FRONTEND]     },
[2026-03-26 21:05:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:05:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:05:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:05:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:05:13] [FRONTEND]       errno: -61,
[2026-03-26 21:05:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:05:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:05:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:05:13] [FRONTEND]       port: 5001
[2026-03-26 21:05:13] [FRONTEND]     }
[2026-03-26 21:05:13] [FRONTEND]   ]
[2026-03-26 21:05:13] [FRONTEND] }
[2026-03-26 21:05:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:05:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:05:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:05:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:05:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:05:13] [FRONTEND]   [errors]: [
[2026-03-26 21:05:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:05:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:05:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:05:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:05:13] [FRONTEND]       errno: -61,
[2026-03-26 21:05:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:05:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:05:13] [FRONTEND]       address: '::1',
[2026-03-26 21:05:13] [FRONTEND]       port: 5001
[2026-03-26 21:05:13] [FRONTEND]     },
[2026-03-26 21:05:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:05:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:05:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:05:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:05:13] [FRONTEND]       errno: -61,
[2026-03-26 21:05:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:05:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:05:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:05:13] [FRONTEND]       port: 5001
[2026-03-26 21:05:13] [FRONTEND]     }
[2026-03-26 21:05:13] [FRONTEND]   ]
[2026-03-26 21:05:13] [FRONTEND] }
[2026-03-26 21:06:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:06:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:06:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:06:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:06:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:06:13] [FRONTEND]   [errors]: [
[2026-03-26 21:06:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:06:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:06:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:06:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:06:13] [FRONTEND]       errno: -61,
[2026-03-26 21:06:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:06:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:06:13] [FRONTEND]       address: '::1',
[2026-03-26 21:06:13] [FRONTEND]       port: 5001
[2026-03-26 21:06:13] [FRONTEND]     },
[2026-03-26 21:06:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:06:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:06:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:06:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:06:13] [FRONTEND]       errno: -61,
[2026-03-26 21:06:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:06:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:06:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:06:13] [FRONTEND]       port: 5001
[2026-03-26 21:06:13] [FRONTEND]     }
[2026-03-26 21:06:13] [FRONTEND]   ]
[2026-03-26 21:06:13] [FRONTEND] }
[2026-03-26 21:06:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:06:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:06:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:06:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:06:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:06:13] [FRONTEND]   [errors]: [
[2026-03-26 21:06:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:06:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:06:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:06:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:06:13] [FRONTEND]       errno: -61,
[2026-03-26 21:06:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:06:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:06:13] [FRONTEND]       address: '::1',
[2026-03-26 21:06:13] [FRONTEND]       port: 5001
[2026-03-26 21:06:13] [FRONTEND]     },
[2026-03-26 21:06:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:06:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:06:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:06:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:06:13] [FRONTEND]       errno: -61,
[2026-03-26 21:06:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:06:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:06:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:06:13] [FRONTEND]       port: 5001
[2026-03-26 21:06:13] [FRONTEND]     }
[2026-03-26 21:06:13] [FRONTEND]   ]
[2026-03-26 21:06:13] [FRONTEND] }
[2026-03-26 21:07:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:07:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:07:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:07:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:07:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:07:13] [FRONTEND]   [errors]: [
[2026-03-26 21:07:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:07:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:07:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:07:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:07:13] [FRONTEND]       errno: -61,
[2026-03-26 21:07:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:07:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:07:13] [FRONTEND]       address: '::1',
[2026-03-26 21:07:13] [FRONTEND]       port: 5001
[2026-03-26 21:07:13] [FRONTEND]     },
[2026-03-26 21:07:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:07:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:07:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:07:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:07:13] [FRONTEND]       errno: -61,
[2026-03-26 21:07:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:07:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:07:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:07:13] [FRONTEND]       port: 5001
[2026-03-26 21:07:13] [FRONTEND]     }
[2026-03-26 21:07:13] [FRONTEND]   ]
[2026-03-26 21:07:13] [FRONTEND] }
[2026-03-26 21:07:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:07:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:07:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:07:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:07:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:07:13] [FRONTEND]   [errors]: [
[2026-03-26 21:07:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:07:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:07:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:07:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:07:13] [FRONTEND]       errno: -61,
[2026-03-26 21:07:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:07:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:07:13] [FRONTEND]       address: '::1',
[2026-03-26 21:07:13] [FRONTEND]       port: 5001
[2026-03-26 21:07:13] [FRONTEND]     },
[2026-03-26 21:07:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:07:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:07:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:07:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:07:13] [FRONTEND]       errno: -61,
[2026-03-26 21:07:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:07:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:07:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:07:13] [FRONTEND]       port: 5001
[2026-03-26 21:07:13] [FRONTEND]     }
[2026-03-26 21:07:13] [FRONTEND]   ]
[2026-03-26 21:07:13] [FRONTEND] }
[2026-03-26 21:08:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:08:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:08:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:08:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:08:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:08:13] [FRONTEND]   [errors]: [
[2026-03-26 21:08:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:08:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:08:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:08:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:08:13] [FRONTEND]       errno: -61,
[2026-03-26 21:08:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:08:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:08:13] [FRONTEND]       address: '::1',
[2026-03-26 21:08:13] [FRONTEND]       port: 5001
[2026-03-26 21:08:13] [FRONTEND]     },
[2026-03-26 21:08:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:08:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:08:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:08:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:08:13] [FRONTEND]       errno: -61,
[2026-03-26 21:08:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:08:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:08:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:08:13] [FRONTEND]       port: 5001
[2026-03-26 21:08:13] [FRONTEND]     }
[2026-03-26 21:08:13] [FRONTEND]   ]
[2026-03-26 21:08:13] [FRONTEND] }
[2026-03-26 21:08:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:08:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:08:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:08:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:08:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:08:13] [FRONTEND]   [errors]: [
[2026-03-26 21:08:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:08:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:08:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:08:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:08:13] [FRONTEND]       errno: -61,
[2026-03-26 21:08:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:08:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:08:13] [FRONTEND]       address: '::1',
[2026-03-26 21:08:13] [FRONTEND]       port: 5001
[2026-03-26 21:08:13] [FRONTEND]     },
[2026-03-26 21:08:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:08:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:08:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:08:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:08:13] [FRONTEND]       errno: -61,
[2026-03-26 21:08:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:08:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:08:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:08:13] [FRONTEND]       port: 5001
[2026-03-26 21:08:13] [FRONTEND]     }
[2026-03-26 21:08:13] [FRONTEND]   ]
[2026-03-26 21:08:13] [FRONTEND] }
[2026-03-26 21:09:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:09:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:09:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:09:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:09:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:09:13] [FRONTEND]   [errors]: [
[2026-03-26 21:09:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:09:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:09:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:09:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:09:13] [FRONTEND]       errno: -61,
[2026-03-26 21:09:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:09:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:09:13] [FRONTEND]       address: '::1',
[2026-03-26 21:09:13] [FRONTEND]       port: 5001
[2026-03-26 21:09:13] [FRONTEND]     },
[2026-03-26 21:09:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:09:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:09:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:09:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:09:13] [FRONTEND]       errno: -61,
[2026-03-26 21:09:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:09:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:09:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:09:13] [FRONTEND]       port: 5001
[2026-03-26 21:09:13] [FRONTEND]     }
[2026-03-26 21:09:13] [FRONTEND]   ]
[2026-03-26 21:09:13] [FRONTEND] }
[2026-03-26 21:09:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:09:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:09:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:09:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:09:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:09:13] [FRONTEND]   [errors]: [
[2026-03-26 21:09:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:09:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:09:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:09:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:09:13] [FRONTEND]       errno: -61,
[2026-03-26 21:09:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:09:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:09:13] [FRONTEND]       address: '::1',
[2026-03-26 21:09:13] [FRONTEND]       port: 5001
[2026-03-26 21:09:13] [FRONTEND]     },
[2026-03-26 21:09:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:09:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:09:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:09:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:09:13] [FRONTEND]       errno: -61,
[2026-03-26 21:09:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:09:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:09:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:09:13] [FRONTEND]       port: 5001
[2026-03-26 21:09:13] [FRONTEND]     }
[2026-03-26 21:09:13] [FRONTEND]   ]
[2026-03-26 21:09:13] [FRONTEND] }
[2026-03-26 21:10:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:10:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:10:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:10:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:10:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:10:13] [FRONTEND]   [errors]: [
[2026-03-26 21:10:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:10:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:10:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:10:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:10:13] [FRONTEND]       errno: -61,
[2026-03-26 21:10:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:10:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:10:13] [FRONTEND]       address: '::1',
[2026-03-26 21:10:13] [FRONTEND]       port: 5001
[2026-03-26 21:10:13] [FRONTEND]     },
[2026-03-26 21:10:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:10:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:10:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:10:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:10:13] [FRONTEND]       errno: -61,
[2026-03-26 21:10:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:10:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:10:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:10:13] [FRONTEND]       port: 5001
[2026-03-26 21:10:13] [FRONTEND]     }
[2026-03-26 21:10:13] [FRONTEND]   ]
[2026-03-26 21:10:13] [FRONTEND] }
[2026-03-26 21:10:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:10:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:10:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:10:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:10:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:10:13] [FRONTEND]   [errors]: [
[2026-03-26 21:10:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:10:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:10:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:10:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:10:13] [FRONTEND]       errno: -61,
[2026-03-26 21:10:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:10:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:10:13] [FRONTEND]       address: '::1',
[2026-03-26 21:10:13] [FRONTEND]       port: 5001
[2026-03-26 21:10:13] [FRONTEND]     },
[2026-03-26 21:10:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:10:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:10:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:10:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:10:13] [FRONTEND]       errno: -61,
[2026-03-26 21:10:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:10:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:10:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:10:13] [FRONTEND]       port: 5001
[2026-03-26 21:10:13] [FRONTEND]     }
[2026-03-26 21:10:13] [FRONTEND]   ]
[2026-03-26 21:10:13] [FRONTEND] }
[2026-03-26 21:11:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:11:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:11:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:11:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:11:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:11:13] [FRONTEND]   [errors]: [
[2026-03-26 21:11:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:11:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:11:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:11:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:11:13] [FRONTEND]       errno: -61,
[2026-03-26 21:11:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:11:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:11:13] [FRONTEND]       address: '::1',
[2026-03-26 21:11:13] [FRONTEND]       port: 5001
[2026-03-26 21:11:13] [FRONTEND]     },
[2026-03-26 21:11:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:11:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:11:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:11:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:11:13] [FRONTEND]       errno: -61,
[2026-03-26 21:11:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:11:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:11:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:11:13] [FRONTEND]       port: 5001
[2026-03-26 21:11:13] [FRONTEND]     }
[2026-03-26 21:11:13] [FRONTEND]   ]
[2026-03-26 21:11:13] [FRONTEND] }
[2026-03-26 21:11:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:11:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:11:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:11:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:11:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:11:13] [FRONTEND]   [errors]: [
[2026-03-26 21:11:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:11:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:11:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:11:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:11:13] [FRONTEND]       errno: -61,
[2026-03-26 21:11:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:11:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:11:13] [FRONTEND]       address: '::1',
[2026-03-26 21:11:13] [FRONTEND]       port: 5001
[2026-03-26 21:11:13] [FRONTEND]     },
[2026-03-26 21:11:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:11:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:11:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:11:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:11:13] [FRONTEND]       errno: -61,
[2026-03-26 21:11:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:11:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:11:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:11:13] [FRONTEND]       port: 5001
[2026-03-26 21:11:13] [FRONTEND]     }
[2026-03-26 21:11:13] [FRONTEND]   ]
[2026-03-26 21:11:13] [FRONTEND] }
[2026-03-26 21:12:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:12:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:12:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:12:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:12:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:12:13] [FRONTEND]   [errors]: [
[2026-03-26 21:12:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:12:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:12:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:12:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:12:13] [FRONTEND]       errno: -61,
[2026-03-26 21:12:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:12:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:12:13] [FRONTEND]       address: '::1',
[2026-03-26 21:12:13] [FRONTEND]       port: 5001
[2026-03-26 21:12:13] [FRONTEND]     },
[2026-03-26 21:12:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:12:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:12:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:12:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:12:13] [FRONTEND]       errno: -61,
[2026-03-26 21:12:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:12:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:12:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:12:13] [FRONTEND]       port: 5001
[2026-03-26 21:12:13] [FRONTEND]     }
[2026-03-26 21:12:13] [FRONTEND]   ]
[2026-03-26 21:12:13] [FRONTEND] }
[2026-03-26 21:12:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:12:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:12:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:12:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:12:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:12:13] [FRONTEND]   [errors]: [
[2026-03-26 21:12:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:12:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:12:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:12:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:12:13] [FRONTEND]       errno: -61,
[2026-03-26 21:12:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:12:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:12:13] [FRONTEND]       address: '::1',
[2026-03-26 21:12:13] [FRONTEND]       port: 5001
[2026-03-26 21:12:13] [FRONTEND]     },
[2026-03-26 21:12:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:12:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:12:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:12:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:12:13] [FRONTEND]       errno: -61,
[2026-03-26 21:12:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:12:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:12:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:12:13] [FRONTEND]       port: 5001
[2026-03-26 21:12:13] [FRONTEND]     }
[2026-03-26 21:12:13] [FRONTEND]   ]
[2026-03-26 21:12:13] [FRONTEND] }
[2026-03-26 21:13:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:13:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:13:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:13:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:13:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:13:13] [FRONTEND]   [errors]: [
[2026-03-26 21:13:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:13:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:13:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:13:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:13:13] [FRONTEND]       errno: -61,
[2026-03-26 21:13:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:13:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:13:13] [FRONTEND]       address: '::1',
[2026-03-26 21:13:13] [FRONTEND]       port: 5001
[2026-03-26 21:13:13] [FRONTEND]     },
[2026-03-26 21:13:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:13:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:13:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:13:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:13:13] [FRONTEND]       errno: -61,
[2026-03-26 21:13:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:13:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:13:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:13:13] [FRONTEND]       port: 5001
[2026-03-26 21:13:13] [FRONTEND]     }
[2026-03-26 21:13:13] [FRONTEND]   ]
[2026-03-26 21:13:13] [FRONTEND] }
[2026-03-26 21:13:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:13:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:13:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:13:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:13:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:13:13] [FRONTEND]   [errors]: [
[2026-03-26 21:13:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:13:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:13:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:13:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:13:13] [FRONTEND]       errno: -61,
[2026-03-26 21:13:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:13:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:13:13] [FRONTEND]       address: '::1',
[2026-03-26 21:13:13] [FRONTEND]       port: 5001
[2026-03-26 21:13:13] [FRONTEND]     },
[2026-03-26 21:13:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:13:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:13:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:13:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:13:13] [FRONTEND]       errno: -61,
[2026-03-26 21:13:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:13:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:13:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:13:13] [FRONTEND]       port: 5001
[2026-03-26 21:13:13] [FRONTEND]     }
[2026-03-26 21:13:13] [FRONTEND]   ]
[2026-03-26 21:13:13] [FRONTEND] }
[2026-03-26 21:14:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:14:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:14:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:14:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:14:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:14:13] [FRONTEND]   [errors]: [
[2026-03-26 21:14:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:14:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:14:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:14:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:14:13] [FRONTEND]       errno: -61,
[2026-03-26 21:14:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:14:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:14:13] [FRONTEND]       address: '::1',
[2026-03-26 21:14:13] [FRONTEND]       port: 5001
[2026-03-26 21:14:13] [FRONTEND]     },
[2026-03-26 21:14:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:14:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:14:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:14:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:14:13] [FRONTEND]       errno: -61,
[2026-03-26 21:14:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:14:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:14:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:14:13] [FRONTEND]       port: 5001
[2026-03-26 21:14:13] [FRONTEND]     }
[2026-03-26 21:14:13] [FRONTEND]   ]
[2026-03-26 21:14:13] [FRONTEND] }
[2026-03-26 21:14:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:14:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:14:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:14:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:14:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:14:13] [FRONTEND]   [errors]: [
[2026-03-26 21:14:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:14:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:14:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:14:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:14:13] [FRONTEND]       errno: -61,
[2026-03-26 21:14:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:14:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:14:13] [FRONTEND]       address: '::1',
[2026-03-26 21:14:13] [FRONTEND]       port: 5001
[2026-03-26 21:14:13] [FRONTEND]     },
[2026-03-26 21:14:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:14:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:14:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:14:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:14:13] [FRONTEND]       errno: -61,
[2026-03-26 21:14:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:14:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:14:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:14:13] [FRONTEND]       port: 5001
[2026-03-26 21:14:13] [FRONTEND]     }
[2026-03-26 21:14:13] [FRONTEND]   ]
[2026-03-26 21:14:13] [FRONTEND] }
[2026-03-26 21:15:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:15:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:15:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:15:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:15:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:15:13] [FRONTEND]   [errors]: [
[2026-03-26 21:15:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:15:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:15:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:15:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:15:13] [FRONTEND]       errno: -61,
[2026-03-26 21:15:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:15:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:15:13] [FRONTEND]       address: '::1',
[2026-03-26 21:15:13] [FRONTEND]       port: 5001
[2026-03-26 21:15:13] [FRONTEND]     },
[2026-03-26 21:15:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:15:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:15:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:15:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:15:13] [FRONTEND]       errno: -61,
[2026-03-26 21:15:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:15:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:15:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:15:13] [FRONTEND]       port: 5001
[2026-03-26 21:15:13] [FRONTEND]     }
[2026-03-26 21:15:13] [FRONTEND]   ]
[2026-03-26 21:15:13] [FRONTEND] }
[2026-03-26 21:15:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:15:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:15:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:15:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:15:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:15:13] [FRONTEND]   [errors]: [
[2026-03-26 21:15:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:15:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:15:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:15:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:15:13] [FRONTEND]       errno: -61,
[2026-03-26 21:15:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:15:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:15:13] [FRONTEND]       address: '::1',
[2026-03-26 21:15:13] [FRONTEND]       port: 5001
[2026-03-26 21:15:13] [FRONTEND]     },
[2026-03-26 21:15:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:15:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:15:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:15:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:15:13] [FRONTEND]       errno: -61,
[2026-03-26 21:15:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:15:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:15:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:15:13] [FRONTEND]       port: 5001
[2026-03-26 21:15:13] [FRONTEND]     }
[2026-03-26 21:15:13] [FRONTEND]   ]
[2026-03-26 21:15:13] [FRONTEND] }
[2026-03-26 21:16:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:16:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:16:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:16:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:16:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:16:13] [FRONTEND]   [errors]: [
[2026-03-26 21:16:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:16:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:16:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:16:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:16:13] [FRONTEND]       errno: -61,
[2026-03-26 21:16:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:16:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:16:13] [FRONTEND]       address: '::1',
[2026-03-26 21:16:13] [FRONTEND]       port: 5001
[2026-03-26 21:16:13] [FRONTEND]     },
[2026-03-26 21:16:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:16:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:16:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:16:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:16:13] [FRONTEND]       errno: -61,
[2026-03-26 21:16:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:16:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:16:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:16:13] [FRONTEND]       port: 5001
[2026-03-26 21:16:13] [FRONTEND]     }
[2026-03-26 21:16:13] [FRONTEND]   ]
[2026-03-26 21:16:13] [FRONTEND] }
[2026-03-26 21:16:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:16:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:16:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-26 21:16:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:16:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:16:13] [FRONTEND]   [errors]: [
[2026-03-26 21:16:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:16:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:16:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:16:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:16:13] [FRONTEND]       errno: -61,
[2026-03-26 21:16:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:16:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:16:13] [FRONTEND]       address: '::1',
[2026-03-26 21:16:13] [FRONTEND]       port: 5001
[2026-03-26 21:16:13] [FRONTEND]     },
[2026-03-26 21:16:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:16:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:16:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-26 21:16:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-26 21:16:13] [FRONTEND]       errno: -61,
[2026-03-26 21:16:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:16:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:16:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:16:13] [FRONTEND]       port: 5001
[2026-03-26 21:16:13] [FRONTEND]     }
[2026-03-26 21:16:13] [FRONTEND]   ]
[2026-03-26 21:16:13] [FRONTEND] }


---
**YENİ OTURUM BAŞLADI:** Thu Mar 26 21:16:57 +03 2026
---

[2026-03-26 21:16:58] [BACKEND] >>> Sicilius Backend Startup Sequence Initiated <<<
[2026-03-26 21:16:59] [BACKEND] [+] Yeni SSH database tüneli kuruluyor. Uzak veritabanı IP'si bulunuyor...
[2026-03-26 21:16:59] [FRONTEND] yarn run v1.22.22
[2026-03-26 21:16:59] [FRONTEND] $ next dev
[2026-03-26 21:16:59] [FRONTEND]   ▲ Next.js 14.2.3
[2026-03-26 21:16:59] [FRONTEND]   - Local:        http://localhost:3000
[2026-03-26 21:16:59] [FRONTEND]   - Environments: .env.local
[2026-03-26 21:16:59] [FRONTEND] 
[2026-03-26 21:16:59] [FRONTEND]  ✓ Starting...
[2026-03-26 21:17:02] [DOCLING] 2026-03-26 21:17:02,444 - INFO - No GPU detected, using CPU.
[2026-03-26 21:17:02] [DOCLING] 2026-03-26 21:17:02,444 - INFO - Starting Docling Fast Server on http://0.0.0.0:5002
[2026-03-26 21:17:02] [DOCLING] 2026-03-26 21:17:02,444 - INFO - OCR settings: force_ocr=False, lang=default
[2026-03-26 21:17:02] [DOCLING] INFO:     Started server process [13324]
[2026-03-26 21:17:02] [DOCLING] INFO:     Waiting for application startup.
[2026-03-26 21:17:02] [DOCLING] 2026-03-26 21:17:02,578 - INFO - Initializing DocumentConverter (force_ocr=False, lang=default, enrichments=none)...
[2026-03-26 21:17:03] [BACKEND] [+] Remote database IP found: 172.18.0.2. Establishing tunnel...
[2026-03-26 21:17:03] [BACKEND] [+] SSH Tunnel successfully established to 172.18.0.2.
[2026-03-26 21:17:03] [BACKEND] [+] Starting FastAPI server...
[2026-03-26 21:17:03] [FRONTEND]  ✓ Ready in 3.8s
[2026-03-26 21:17:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-26 21:17:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:17:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-26 21:17:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:17:13] [FRONTEND]   [errors]: [
[2026-03-26 21:17:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:17:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:17:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-26 21:17:13] [FRONTEND]       errno: -61,
[2026-03-26 21:17:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:17:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:17:13] [FRONTEND]       address: '::1',
[2026-03-26 21:17:13] [FRONTEND]       port: 5001
[2026-03-26 21:17:13] [FRONTEND]     },
[2026-03-26 21:17:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:17:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:17:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-26 21:17:13] [FRONTEND]       errno: -61,
[2026-03-26 21:17:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:17:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:17:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:17:13] [FRONTEND]       port: 5001
[2026-03-26 21:17:13] [FRONTEND]     }
[2026-03-26 21:17:13] [FRONTEND]   ]
[2026-03-26 21:17:13] [FRONTEND] }
[2026-03-26 21:17:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-26 21:17:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-26 21:17:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-26 21:17:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-26 21:17:13] [FRONTEND]   [errors]: [
[2026-03-26 21:17:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-26 21:17:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:17:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-26 21:17:13] [FRONTEND]       errno: -61,
[2026-03-26 21:17:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:17:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:17:13] [FRONTEND]       address: '::1',
[2026-03-26 21:17:13] [FRONTEND]       port: 5001
[2026-03-26 21:17:13] [FRONTEND]     },
[2026-03-26 21:17:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-26 21:17:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-26 21:17:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-26 21:17:13] [FRONTEND]       errno: -61,
[2026-03-26 21:17:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-26 21:17:13] [FRONTEND]       syscall: 'connect',
[2026-03-26 21:17:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-26 21:17:13] [FRONTEND]       port: 5001
[2026-03-26 21:17:13] [FRONTEND]     }
[2026-03-26 21:17:13] [FRONTEND]   ]
[2026-03-26 21:17:13] [FRONTEND] }
[2026-03-26 21:17:13] [FRONTEND]  ✓ Compiled /_error in 277ms (259 modules)
[2026-03-26 21:17:19] [DOCLING] 2026-03-26 21:17:19,039 - INFO - DocumentConverter initialized in 16.46s
[2026-03-26 21:17:19] [DOCLING] INFO:     Application startup complete.
[2026-03-26 21:17:19] [DOCLING] ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 5002): address already in use
[2026-03-26 21:17:19] [DOCLING] INFO:     Waiting for application shutdown.
[2026-03-26 21:17:19] [DOCLING] INFO:     Application shutdown complete.
[2026-03-26 21:17:19] [BACKEND] INFO:     Started server process [13346]
[2026-03-26 21:17:19] [BACKEND] INFO:     Waiting for application startup.
[2026-03-26 21:17:19] [DOCLING] cd backend && opendataloader-pdf-hybrid --port 5002 exited with code 1
[2026-03-26 21:17:20] [CELERY]  
[2026-03-26 21:17:20] [CELERY]  -------------- celery@192.168.1.8 v5.3.4 (emerald-rush)
[2026-03-26 21:17:20] [CELERY] --- ***** ----- 
[2026-03-26 21:17:20] [CELERY] -- ******* ---- macOS-26.3.1-arm64-arm-64bit 2026-03-26 21:17:20
[2026-03-26 21:17:20] [CELERY] - *** --- * --- 
[2026-03-26 21:17:20] [CELERY] - ** ---------- [config]
[2026-03-26 21:17:20] [CELERY] - ** ---------- .> app:         worker:0x10b82e170
[2026-03-26 21:17:20] [CELERY] - ** ---------- .> transport:   redis://localhost:6379/0
[2026-03-26 21:17:20] [CELERY] - ** ---------- .> results:     redis://localhost:6379/0
[2026-03-26 21:17:20] [CELERY] - *** --- * --- .> concurrency: 8 (solo)
[2026-03-26 21:17:20] [CELERY] -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
[2026-03-26 21:17:20] [CELERY] --- ***** ----- 
[2026-03-26 21:17:20] [CELERY]  -------------- [queues]
[2026-03-26 21:17:20] [CELERY]                 .> celery           exchange=celery(direct) key=celery
[2026-03-26 21:17:20] [CELERY]                 
[2026-03-26 21:17:20] [CELERY] 
[2026-03-26 21:17:20] [CELERY] [tasks]
[2026-03-26 21:17:20] [CELERY]   . app.tasks.ocr_tasks.run_historical_ocr_backfill
[2026-03-26 21:17:20] [CELERY]   . app.tasks.scraping_tasks.run_scraping_task
[2026-03-26 21:17:20] [CELERY] 
[2026-03-26 21:17:20] [CELERY] 2026-03-26 21:17:20,347 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-26 21:17:20] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-26 21:17:20] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-26 21:17:20] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-26 21:17:20] [CELERY]   warnings.warn(
[2026-03-26 21:17:20] [CELERY] 
[2026-03-26 21:17:20] [CELERY] 2026-03-26 21:17:20,363 - celery.worker.consumer.connection - INFO - Connected to redis://localhost:6379/0
[2026-03-26 21:17:20] [CELERY] 2026-03-26 21:17:20,363 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-26 21:17:20] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-26 21:17:20] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-26 21:17:20] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-26 21:17:20] [CELERY]   warnings.warn(
[2026-03-26 21:17:20] [CELERY] 
[2026-03-26 21:17:20] [CELERY] 2026-03-26 21:17:20,364 - celery.worker.consumer.mingle - INFO - mingle: searching for neighbors
[2026-03-26 21:17:21] [BACKEND] INFO:     Application startup complete.
[2026-03-26 21:17:21] [BACKEND] INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
[2026-03-26 21:17:21] [CELERY] 2026-03-26 21:17:21,372 - celery.worker.consumer.mingle - INFO - mingle: all alone
[2026-03-26 21:17:21] [CELERY] 2026-03-26 21:17:21,389 - celery.apps.worker - INFO - celery@192.168.1.8 ready.
[2026-03-26 21:25:05] [FRONTEND]  ✓ Compiled /src/middleware in 77ms (73 modules)
[2026-03-26 21:25:05] [FRONTEND]  ○ Compiling /login ...
[2026-03-26 21:25:07] [FRONTEND]  ✓ Compiled /login in 1752ms (4557 modules)
[2026-03-26 21:25:07] [FRONTEND]  GET /login/?callbackUrl=%2Fadmin%2Focr-management%2F 200 in 2060ms
[2026-03-26 21:25:07] [FRONTEND]  ○ Compiling /manifest.webmanifest ...
[2026-03-26 21:25:07] [FRONTEND]  ✓ Compiled /manifest.webmanifest in 530ms (4593 modules)
[2026-03-26 21:25:08] [FRONTEND]  GET /manifest.webmanifest 200 in 762ms
[2026-03-26 21:25:08] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 780ms
[2026-03-26 21:25:14] [BACKEND] 2026-03-26 21:25:14,535 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:25:15] [FRONTEND]  ○ Compiling /admin ...
[2026-03-26 21:25:16] [FRONTEND]  ✓ Compiled /admin in 1599ms (6044 modules)
[2026-03-26 21:25:16] [BACKEND] 2026-03-26 21:25:16,352 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:25:16] [FRONTEND]  GET /manifest.webmanifest 200 in 16ms
[2026-03-26 21:25:16] [BACKEND] DEBUG: require-admin entered for turgaykirkil@me.com
[2026-03-26 21:25:16] [BACKEND] DEBUG: require-admin check: is_admin=True
[2026-03-26 21:25:16] [BACKEND] 2026-03-26 21:25:16,783 - app.api.api_v1.endpoints.auth - WARNING - [require-admin] user=turgaykirkil@me.com role=admin is_admin=True
[2026-03-26 21:25:16] [BACKEND] DEBUG: require-admin entered for turgaykirkil@me.com
[2026-03-26 21:25:16] [BACKEND] DEBUG: require-admin check: is_admin=True
[2026-03-26 21:25:16] [BACKEND] 2026-03-26 21:25:16,981 - app.api.api_v1.endpoints.auth - WARNING - [require-admin] user=turgaykirkil@me.com role=admin is_admin=True
[2026-03-26 21:25:18] [FRONTEND]  ○ Compiling /dashboard ...
[2026-03-26 21:25:19] [FRONTEND]  ✓ Compiled /dashboard in 1596ms (8262 modules)
[2026-03-26 21:25:20] [FRONTEND]  GET /dashboard/ 200 in 1771ms
[2026-03-26 21:25:20] [FRONTEND]  GET /manifest.webmanifest 200 in 29ms
[2026-03-26 21:25:21] [BACKEND] 2026-03-26 21:25:21,078 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:25:21] [BACKEND] 2026-03-26 21:25:21,174 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:25:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:25:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:25:33] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 28ms
[2026-03-26 21:25:33] [FRONTEND]  GET /manifest.webmanifest 200 in 33ms
[2026-03-26 21:25:49] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:26:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:27:23] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:28:23] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:29:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:30:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:31:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:32:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:33:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:36:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:38:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:39:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:40:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:40:34] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:40:39] [FRONTEND]  GET /dashboard/ 200 in 34ms
[2026-03-26 21:40:39] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 62ms
[2026-03-26 21:40:39] [FRONTEND]  GET /manifest.webmanifest 200 in 83ms
[2026-03-26 21:40:39] [BACKEND] 2026-03-26 21:40:39,792 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:40:39] [BACKEND] 2026-03-26 21:40:39,922 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:40:39] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:40:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:40:43] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:40:48] [FRONTEND]  GET /dashboard/ 200 in 29ms
[2026-03-26 21:40:48] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 31ms
[2026-03-26 21:40:48] [FRONTEND]  GET /manifest.webmanifest 200 in 40ms
[2026-03-26 21:40:49] [BACKEND] 2026-03-26 21:40:49,192 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:40:49] [BACKEND] 2026-03-26 21:40:49,322 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:40:49] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:40:49] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:40:52] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa


---
**YENİ OTURUM BAŞLADI:** Thu Mar 26 21:41:03 +03 2026
---

[2026-03-26 21:41:04] [BACKEND] >>> Sicilius Backend Startup Sequence Initiated <<<
[2026-03-26 21:41:04] [FRONTEND] yarn run v1.22.22
[2026-03-26 21:41:04] [BACKEND] [+] Eski (zombi) SSH tüneli bulundu, temizleniyor...
[2026-03-26 21:41:04] [FRONTEND] $ next dev
[2026-03-26 21:41:05] [FRONTEND]   ▲ Next.js 14.2.3
[2026-03-26 21:41:05] [FRONTEND]   - Local:        http://localhost:3000
[2026-03-26 21:41:05] [FRONTEND]   - Environments: .env.local
[2026-03-26 21:41:05] [FRONTEND] 
[2026-03-26 21:41:05] [FRONTEND]  ✓ Starting...
[2026-03-26 21:41:05] [DOCLING] 2026-03-26 21:41:05,376 - INFO - No GPU detected, using CPU.
[2026-03-26 21:41:05] [DOCLING] 2026-03-26 21:41:05,377 - INFO - Starting Docling Fast Server on http://0.0.0.0:5002
[2026-03-26 21:41:05] [DOCLING] 2026-03-26 21:41:05,377 - INFO - OCR settings: force_ocr=False, lang=default
[2026-03-26 21:41:05] [DOCLING] INFO:     Started server process [23170]
[2026-03-26 21:41:05] [DOCLING] INFO:     Waiting for application startup.
[2026-03-26 21:41:05] [DOCLING] 2026-03-26 21:41:05,405 - INFO - Initializing DocumentConverter (force_ocr=False, lang=default, enrichments=none)...
[2026-03-26 21:41:05] [BACKEND] [+] Yeni SSH database tüneli kuruluyor. Uzak veritabanı IP'si bulunuyor...
[2026-03-26 21:41:07] [FRONTEND]  ✓ Ready in 1939ms
[2026-03-26 21:41:07] [BACKEND] [+] Remote database IP found: 172.18.0.2. Establishing tunnel...
[2026-03-26 21:41:08] [BACKEND] [+] SSH Tunnel successfully established to 172.18.0.2.
[2026-03-26 21:41:08] [BACKEND] [+] Starting FastAPI server...
[2026-03-26 21:41:11] [DOCLING] 2026-03-26 21:41:11,124 - INFO - DocumentConverter initialized in 5.72s
[2026-03-26 21:41:11] [DOCLING] INFO:     Application startup complete.
[2026-03-26 21:41:11] [DOCLING] ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 5002): address already in use
[2026-03-26 21:41:11] [DOCLING] INFO:     Waiting for application shutdown.
[2026-03-26 21:41:11] [DOCLING] INFO:     Application shutdown complete.
[2026-03-26 21:41:11] [CELERY]  
[2026-03-26 21:41:11] [CELERY]  -------------- celery@192.168.1.8 v5.3.4 (emerald-rush)
[2026-03-26 21:41:11] [CELERY] --- ***** ----- 
[2026-03-26 21:41:11] [CELERY] -- ******* ---- macOS-26.3.1-arm64-arm-64bit 2026-03-26 21:41:11
[2026-03-26 21:41:11] [CELERY] - *** --- * --- 
[2026-03-26 21:41:11] [CELERY] - ** ---------- [config]
[2026-03-26 21:41:11] [CELERY] - ** ---------- .> app:         worker:0x10bd86170
[2026-03-26 21:41:11] [CELERY] - ** ---------- .> transport:   redis://localhost:6379/0
[2026-03-26 21:41:11] [CELERY] - ** ---------- .> results:     redis://localhost:6379/0
[2026-03-26 21:41:11] [CELERY] - *** --- * --- .> concurrency: 8 (solo)
[2026-03-26 21:41:11] [CELERY] -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
[2026-03-26 21:41:11] [CELERY] --- ***** ----- 
[2026-03-26 21:41:11] [CELERY]  -------------- [queues]
[2026-03-26 21:41:11] [CELERY]                 .> celery           exchange=celery(direct) key=celery
[2026-03-26 21:41:11] [CELERY]                 
[2026-03-26 21:41:11] [CELERY] 
[2026-03-26 21:41:11] [CELERY] [tasks]
[2026-03-26 21:41:11] [CELERY]   . app.tasks.ocr_tasks.run_historical_ocr_backfill
[2026-03-26 21:41:11] [CELERY]   . app.tasks.scraping_tasks.run_scraping_task
[2026-03-26 21:41:11] [CELERY] 
[2026-03-26 21:41:11] [CELERY] 2026-03-26 21:41:11,876 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-26 21:41:11] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-26 21:41:11] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-26 21:41:11] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-26 21:41:11] [CELERY]   warnings.warn(
[2026-03-26 21:41:11] [CELERY] 
[2026-03-26 21:41:11] [CELERY] 2026-03-26 21:41:11,880 - celery.worker.consumer.connection - INFO - Connected to redis://localhost:6379/0
[2026-03-26 21:41:11] [CELERY] 2026-03-26 21:41:11,880 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-26 21:41:11] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-26 21:41:11] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-26 21:41:11] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-26 21:41:11] [CELERY]   warnings.warn(
[2026-03-26 21:41:11] [CELERY] 
[2026-03-26 21:41:11] [CELERY] 2026-03-26 21:41:11,882 - celery.worker.consumer.mingle - INFO - mingle: searching for neighbors
[2026-03-26 21:41:12] [DOCLING] cd backend && opendataloader-pdf-hybrid --port 5002 exited with code 1
[2026-03-26 21:41:12] [CELERY] 2026-03-26 21:41:12,892 - celery.worker.consumer.mingle - INFO - mingle: all alone
[2026-03-26 21:41:12] [CELERY] 2026-03-26 21:41:12,898 - celery.apps.worker - INFO - celery@192.168.1.8 ready.
[2026-03-26 21:41:15] [BACKEND] INFO:     Started server process [23218]
[2026-03-26 21:41:15] [BACKEND] INFO:     Waiting for application startup.
[2026-03-26 21:41:16] [BACKEND] INFO:     Application startup complete.
[2026-03-26 21:41:16] [BACKEND] INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
[2026-03-26 21:41:29] [FRONTEND]  ✓ Compiled /src/middleware in 83ms (73 modules)
[2026-03-26 21:41:29] [FRONTEND]  ○ Compiling /dashboard ...
[2026-03-26 21:41:31] [FRONTEND]  ✓ Compiled /dashboard in 2.2s (4522 modules)
[2026-03-26 21:41:31] [FRONTEND]  GET /dashboard/ 200 in 2460ms
[2026-03-26 21:41:32] [FRONTEND]  ○ Compiling /manifest.webmanifest ...
[2026-03-26 21:41:32] [FRONTEND]  ✓ Compiled /manifest.webmanifest in 705ms (4558 modules)
[2026-03-26 21:41:32] [BACKEND] 2026-03-26 21:41:32,501 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:41:32] [BACKEND] 2026-03-26 21:41:32,612 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 21:41:32] [FRONTEND]  GET /manifest.webmanifest 200 in 1001ms
[2026-03-26 21:41:32] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 992ms
[2026-03-26 21:41:32] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:41:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:41:37] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:41:42] [FRONTEND]  ✓ Compiled /api/v1/search/company-detail in 357ms (2364 modules)
[2026-03-26 21:41:43] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=a6b218dd-5c1d-4ee7-b24e-fb4749100747 200 in 1286ms
[2026-03-26 21:41:43] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:42:32] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:43:18] [BACKEND] 2026-03-26 21:43:18,815 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company a791dc94-02f3-466b-aa55-6b211d9be723: 'Aksi Karar Almnncaya Kadar Türkiye Cumhuriyeti Uyruklu 112******42 Kimlik No'lu; ISTANBUL KARTAL'
[2026-03-26 21:43:32] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:44:08] [BACKEND] 2026-03-26 21:44:08,342 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company a791dc94-02f3-466b-aa55-6b211d9be723: 'Aksi Karar Almnncaya Kadar Türkiye Cumhuriyeti Uyruklu 112******42 Kimlik No'lu; ISTANBUL KARTAL'
[2026-03-26 21:44:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:44:35] [BACKEND] 2026-03-26 21:44:35,829 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company a791dc94-02f3-466b-aa55-6b211d9be723: 'Aksi Karar Almnncaya Kadar Türkiye Cumhuriyeti Uyruklu 112******42 Kimlik No'lu; ISTANBUL KARTAL'
[2026-03-26 21:44:39] [BACKEND] 2026-03-26 21:44:39,640 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company a791dc94-02f3-466b-aa55-6b211d9be723: 'Aksi Karar Almnncaya Kadar Türkiye Cumhuriyeti Uyruklu 112******42 Kimlik No'lu; ISTANBUL KARTAL'
[2026-03-26 21:45:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:46:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:47:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:50:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:52:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:54:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:56:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:58:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 21:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:00:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:02:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:04:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:06:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:08:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:09:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:10:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:12:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:14:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:16:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:18:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:20:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:21:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:22:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:24:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:26:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:27:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:28:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:30:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:32:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:33:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:34:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:35:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:36:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:38:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:39:25] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:40:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:42:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:43:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:44:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:46:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:48:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:50:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:52:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:54:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:56:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:56:46] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:56:56] [FRONTEND]  GET /dashboard/ 200 in 168ms
[2026-03-26 22:56:56] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 27ms
[2026-03-26 22:56:56] [FRONTEND]  GET /manifest.webmanifest 200 in 63ms
[2026-03-26 22:56:57] [BACKEND] 2026-03-26 22:56:57,399 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 22:56:57] [BACKEND] 2026-03-26 22:56:57,550 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-26 22:56:57] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:56:57] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:57:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:57:07] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 200 in 3426ms
[2026-03-26 22:57:07] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:57:57] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:57:57] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:57:59] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 200 in 637ms
[2026-03-26 22:57:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:58:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 22:59:58] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:01:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:01:58] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:02:58] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:04:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:06:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:06:58] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:08:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:10:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:11:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:12:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:14:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:16:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:17:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:18:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:20:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:22:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:24:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:25:31] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:26:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:28:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:30:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:31:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:32:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:34:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:36:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:37:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:38:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:40:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:42:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:43:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:44:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:46:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:48:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:50:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:52:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:54:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:56:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:58:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-26 23:58:58] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:00:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:01:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:02:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:03:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:04:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:06:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:08:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:10:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:12:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:14:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:15:03] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:15:08] [FRONTEND]  GET /dashboard/ 200 in 31ms
[2026-03-27 00:15:08] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 40ms
[2026-03-27 00:15:08] [FRONTEND]  GET /manifest.webmanifest 200 in 52ms
[2026-03-27 00:15:14] [BACKEND] 2026-03-27 00:15:14,882 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-27 00:15:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:15:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:15:15] [BACKEND] 2026-03-27 00:15:15,350 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-27 00:15:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:15:24] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 200 in 1186ms
[2026-03-27 00:15:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:15:56] [BACKEND] 2026-03-27 00:15:55,999 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company 340b3ab7-8b32-4d1a-ac90-bcfaeba4470f: 'Sirketin isleri ve islemleri genel kurul tarafindan seçilecek bir veya birkaç müdür tarafindan yürütülür: Aksi Karar Alinmncaya Kadar Türkiye Cumhuriyeti Uyruklu 359******46 Kimlik No'lu, ISTANBUL SANCAKTEPE'
[2026-03-27 00:15:58] [BACKEND] 2026-03-27 00:15:58,987 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company 340b3ab7-8b32-4d1a-ac90-bcfaeba4470f: 'Sirketin isleri ve islemleri genel kurul tarafindan seçilecek bir veya birkaç müdür tarafindan yürütülür: Aksi Karar Alinmncaya Kadar Türkiye Cumhuriyeti Uyruklu 359******46 Kimlik No'lu, ISTANBUL SANCAKTEPE'
[2026-03-27 00:16:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:17:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:18:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:19:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:20:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:21:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 00:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:17:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:21:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:57:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 01:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:29:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:45:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 02:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:01:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:03:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:05:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:39:25] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 03:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:29:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 04:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:29:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 05:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:01:18] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:17:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:33:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:35:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:37:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:55:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 06:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:17:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:23:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:29:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:47:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:51:18] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 07:59:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:01:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:09:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:25:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:55:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 08:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:09:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 09:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:13:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 10:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:01:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:07:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:17:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:45:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 11:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:01:18] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:15:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:21:23] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:35:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:45:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 12:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:03:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:05:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:13:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:39:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:47:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 13:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:05:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:21:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:23:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:35:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:39:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 14:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:09:18] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:15:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:17:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:45:16] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:49:23] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 15:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:15:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:19:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:23:23] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:27:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:41:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:47:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:49:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:57:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 16:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:01:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:03:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:05:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:07:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:09:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:11:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:13:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:15:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:17:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:19:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:21:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:23:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:25:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:27:18] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:29:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:33:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:35:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:37:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:39:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:41:23] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:43:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:45:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:47:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:49:14] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:51:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:53:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:55:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:57:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 17:59:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:04:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:22:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:24:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:26:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:28:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:30:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:32:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:34:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:36:37] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:38:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:40:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:42:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:44:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:46:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:48:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:50:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:52:28] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:54:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:56:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 18:58:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:00:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:02:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:04:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:06:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:08:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:10:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:12:29] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:14:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:16:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:18:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:20:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:22:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:24:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:26:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:28:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:30:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:32:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:34:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:36:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:38:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:40:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:42:35] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:44:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:46:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:48:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:50:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:52:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:54:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:56:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 19:58:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:00:31] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:02:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:04:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:06:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:08:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:10:31] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:12:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:14:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:16:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:18:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:20:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:22:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:24:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:26:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:28:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:30:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:32:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:34:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:36:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:38:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:40:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:42:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:44:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:46:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:48:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:50:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:52:35] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:54:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:56:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 20:58:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:00:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:02:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:04:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:06:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:08:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:10:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:12:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:14:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:16:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:18:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:20:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:22:32] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-27 21:24:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 12:19:00] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 401 in 58ms
[2026-03-28 12:19:01] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 401 in 28ms
[2026-03-28 12:19:04] [FRONTEND]  ○ Compiling /login ...
[2026-03-28 12:19:05] [FRONTEND]  ✓ Compiled /login in 1745ms (7919 modules)
[2026-03-28 12:19:05] [FRONTEND]  GET /login/?callbackUrl=%2Fdashboard%2F 200 in 1880ms
[2026-03-28 12:19:06] [FRONTEND]  ✓ Compiled /manifest.webmanifest in 414ms (7952 modules)
[2026-03-28 12:19:06] [FRONTEND]  GET /manifest.webmanifest 200 in 649ms
[2026-03-28 12:19:06] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 678ms
[2026-03-28 12:19:11] [BACKEND] ERROR:    Exception in ASGI application
[2026-03-28 12:19:11] [BACKEND] Traceback (most recent call last):
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
[2026-03-28 12:19:11] [BACKEND]     self._dbapi_connection = engine.raw_connection()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3292, in raw_connection
[2026-03-28 12:19:11] [BACKEND]     return self.pool.connect()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
[2026-03-28 12:19:11] [BACKEND]     return _ConnectionFairy._checkout(self)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1269, in _checkout
[2026-03-28 12:19:11] [BACKEND]     fairy = _ConnectionRecord.checkout(pool)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 721, in checkout
[2026-03-28 12:19:11] [BACKEND]     with util.safe_reraise():
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 12:19:11] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 719, in checkout
[2026-03-28 12:19:11] [BACKEND]     dbapi_connection = rec.get_connection()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in get_connection
[2026-03-28 12:19:11] [BACKEND]     self.__connect()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
[2026-03-28 12:19:11] [BACKEND]     with util.safe_reraise():
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 12:19:11] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
[2026-03-28 12:19:11] [BACKEND]     self.dbapi_connection = connection = pool._invoke_creator(self)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
[2026-03-28 12:19:11] [BACKEND]     return dialect.connect(*cargs, **cparams)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 616, in connect
[2026-03-28 12:19:11] [BACKEND]     return self.loaded_dbapi.connect(*cargs, **cparams)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
[2026-03-28 12:19:11] [BACKEND]     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
[2026-03-28 12:19:11] [BACKEND] psycopg2.OperationalError: connection to server at "localhost" (::1), port 5433 failed: Connection refused
[2026-03-28 12:19:11] [BACKEND] 	Is the server running on that host and accepting TCP/IP connections?
[2026-03-28 12:19:11] [BACKEND] connection to server at "localhost" (127.0.0.1), port 5433 failed: Connection refused
[2026-03-28 12:19:11] [BACKEND] 	Is the server running on that host and accepting TCP/IP connections?
[2026-03-28 12:19:11] [BACKEND] 
[2026-03-28 12:19:11] [BACKEND] 
[2026-03-28 12:19:11] [BACKEND] The above exception was the direct cause of the following exception:
[2026-03-28 12:19:11] [BACKEND] 
[2026-03-28 12:19:11] [BACKEND] Traceback (most recent call last):
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/protocols/http/httptools_impl.py", line 435, in run_asgi
[2026-03-28 12:19:11] [BACKEND]     result = await app(  # type: ignore[func-returns-value]
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
[2026-03-28 12:19:11] [BACKEND]     return await self.app(scope, receive, send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/applications.py", line 1106, in __call__
[2026-03-28 12:19:11] [BACKEND]     await super().__call__(scope, receive, send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/applications.py", line 122, in __call__
[2026-03-28 12:19:11] [BACKEND]     await self.middleware_stack(scope, receive, send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/errors.py", line 184, in __call__
[2026-03-28 12:19:11] [BACKEND]     raise exc
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/errors.py", line 162, in __call__
[2026-03-28 12:19:11] [BACKEND]     await self.app(scope, receive, _send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/cors.py", line 91, in __call__
[2026-03-28 12:19:11] [BACKEND]     await self.simple_response(scope, receive, send, request_headers=headers)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/cors.py", line 146, in simple_response
[2026-03-28 12:19:11] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/sessions.py", line 86, in __call__
[2026-03-28 12:19:11] [BACKEND]     await self.app(scope, receive, send_wrapper)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 108, in __call__
[2026-03-28 12:19:11] [BACKEND]     response = await self.dispatch_func(request, call_next)
[2026-03-28 12:19:11] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/main.py", line 157, in log_requests
[2026-03-28 12:19:11] [BACKEND]     return await call_next(request)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 84, in call_next
[2026-03-28 12:19:11] [BACKEND]     raise app_exc
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 70, in coro
[2026-03-28 12:19:11] [BACKEND]     await self.app(scope, receive_or_disconnect, send_no_error)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
[2026-03-28 12:19:11] [BACKEND]     return await self.app(scope, receive, send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
[2026-03-28 12:19:11] [BACKEND]     raise exc
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
[2026-03-28 12:19:11] [BACKEND]     await self.app(scope, receive, sender)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 20, in __call__
[2026-03-28 12:19:11] [BACKEND]     raise e
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 17, in __call__
[2026-03-28 12:19:11] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 718, in __call__
[2026-03-28 12:19:11] [BACKEND]     await route.handle(scope, receive, send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 276, in handle
[2026-03-28 12:19:11] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 66, in app
[2026-03-28 12:19:11] [BACKEND]     response = await func(request)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/routing.py", line 274, in app
[2026-03-28 12:19:11] [BACKEND]     raw_response = await run_endpoint_function(
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
[2026-03-28 12:19:11] [BACKEND]     return await dependant.call(**values)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/slowapi/extension.py", line 734, in async_wrapper
[2026-03-28 12:19:11] [BACKEND]     response = await func(*args, **kwargs)  # type: ignore
[2026-03-28 12:19:11] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/api/api_v1/endpoints/auth.py", line 101, in login
[2026-03-28 12:19:11] [BACKEND]     user = crud.user.authenticate(
[2026-03-28 12:19:11] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/crud/crud_user.py", line 60, in authenticate
[2026-03-28 12:19:11] [BACKEND]     user = self.get_by_email(db, email=email)
[2026-03-28 12:19:11] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/crud/crud_user.py", line 23, in get_by_email
[2026-03-28 12:19:11] [BACKEND]     .first()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/query.py", line 2748, in first
[2026-03-28 12:19:11] [BACKEND]     return self.limit(1)._iter().first()  # type: ignore
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/query.py", line 2847, in _iter
[2026-03-28 12:19:11] [BACKEND]     result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2308, in execute
[2026-03-28 12:19:11] [BACKEND]     return self._execute_internal(
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2180, in _execute_internal
[2026-03-28 12:19:11] [BACKEND]     conn = self._connection_for_bind(bind)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2047, in _connection_for_bind
[2026-03-28 12:19:11] [BACKEND]     return trans._connection_for_bind(engine, execution_options)
[2026-03-28 12:19:11] [BACKEND]   File "<string>", line 2, in _connection_for_bind
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go
[2026-03-28 12:19:11] [BACKEND]     ret_value = fn(self, *arg, **kw)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1143, in _connection_for_bind
[2026-03-28 12:19:11] [BACKEND]     conn = bind.connect()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3268, in connect
[2026-03-28 12:19:11] [BACKEND]     return self._connection_cls(self)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 147, in __init__
[2026-03-28 12:19:11] [BACKEND]     Connection._handle_dbapi_exception_noconnection(
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2430, in _handle_dbapi_exception_noconnection
[2026-03-28 12:19:11] [BACKEND]     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
[2026-03-28 12:19:11] [BACKEND]     self._dbapi_connection = engine.raw_connection()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3292, in raw_connection
[2026-03-28 12:19:11] [BACKEND]     return self.pool.connect()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
[2026-03-28 12:19:11] [BACKEND]     return _ConnectionFairy._checkout(self)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1269, in _checkout
[2026-03-28 12:19:11] [BACKEND]     fairy = _ConnectionRecord.checkout(pool)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 721, in checkout
[2026-03-28 12:19:11] [BACKEND]     with util.safe_reraise():
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 12:19:11] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 719, in checkout
[2026-03-28 12:19:11] [BACKEND]     dbapi_connection = rec.get_connection()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in get_connection
[2026-03-28 12:19:11] [BACKEND]     self.__connect()
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
[2026-03-28 12:19:11] [BACKEND]     with util.safe_reraise():
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 12:19:11] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
[2026-03-28 12:19:11] [BACKEND]     self.dbapi_connection = connection = pool._invoke_creator(self)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
[2026-03-28 12:19:11] [BACKEND]     return dialect.connect(*cargs, **cparams)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 616, in connect
[2026-03-28 12:19:11] [BACKEND]     return self.loaded_dbapi.connect(*cargs, **cparams)
[2026-03-28 12:19:11] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
[2026-03-28 12:19:11] [BACKEND]     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
[2026-03-28 12:19:11] [BACKEND] sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5433 failed: Connection refused
[2026-03-28 12:19:11] [BACKEND] 	Is the server running on that host and accepting TCP/IP connections?
[2026-03-28 12:19:11] [BACKEND] connection to server at "localhost" (127.0.0.1), port 5433 failed: Connection refused
[2026-03-28 12:19:11] [BACKEND] 	Is the server running on that host and accepting TCP/IP connections?
[2026-03-28 12:19:11] [BACKEND] 
[2026-03-28 12:19:11] [BACKEND] (Background on this error at: https://sqlalche.me/e/20/e3q8)


---
**YENİ OTURUM BAŞLADI:** Sat Mar 28 12:19:22 +03 2026
---

[2026-03-28 12:19:23] [BACKEND] >>> Sicilius Backend Startup Sequence Initiated <<<
[2026-03-28 12:19:23] [BACKEND] [+] Yeni SSH database tüneli kuruluyor. Uzak veritabanı IP'si bulunuyor...
[2026-03-28 12:19:23] [FRONTEND] yarn run v1.22.22
[2026-03-28 12:19:23] [FRONTEND] $ next dev
[2026-03-28 12:19:24] [FRONTEND]   ▲ Next.js 14.2.3
[2026-03-28 12:19:24] [FRONTEND]   - Local:        http://localhost:3000
[2026-03-28 12:19:24] [FRONTEND]   - Environments: .env.local
[2026-03-28 12:19:24] [FRONTEND] 
[2026-03-28 12:19:24] [FRONTEND]  ✓ Starting...
[2026-03-28 12:19:24] [DOCLING] 2026-03-28 12:19:24,385 - INFO - No GPU detected, using CPU.
[2026-03-28 12:19:24] [DOCLING] 2026-03-28 12:19:24,385 - INFO - Starting Docling Fast Server on http://0.0.0.0:5002
[2026-03-28 12:19:24] [DOCLING] 2026-03-28 12:19:24,385 - INFO - OCR settings: force_ocr=False, lang=default
[2026-03-28 12:19:24] [DOCLING] INFO:     Started server process [3403]
[2026-03-28 12:19:24] [DOCLING] INFO:     Waiting for application startup.
[2026-03-28 12:19:24] [DOCLING] 2026-03-28 12:19:24,412 - INFO - Initializing DocumentConverter (force_ocr=False, lang=default, enrichments=none)...
[2026-03-28 12:19:26] [FRONTEND]  ✓ Ready in 1964ms
[2026-03-28 12:19:30] [DOCLING] 2026-03-28 12:19:30,210 - INFO - DocumentConverter initialized in 5.80s
[2026-03-28 12:19:30] [DOCLING] INFO:     Application startup complete.
[2026-03-28 12:19:30] [DOCLING] ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 5002): address already in use
[2026-03-28 12:19:30] [DOCLING] INFO:     Waiting for application shutdown.
[2026-03-28 12:19:30] [DOCLING] INFO:     Application shutdown complete.
[2026-03-28 12:19:30] [DOCLING] cd backend && opendataloader-pdf-hybrid --port 5002 exited with code 1
[2026-03-28 12:19:31] [CELERY]  
[2026-03-28 12:19:31] [CELERY]  -------------- celery@192.168.1.8 v5.3.4 (emerald-rush)
[2026-03-28 12:19:31] [CELERY] --- ***** ----- 
[2026-03-28 12:19:31] [CELERY] -- ******* ---- macOS-26.3.1-arm64-arm-64bit 2026-03-28 12:19:31
[2026-03-28 12:19:31] [CELERY] - *** --- * --- 
[2026-03-28 12:19:31] [CELERY] - ** ---------- [config]
[2026-03-28 12:19:31] [CELERY] - ** ---------- .> app:         worker:0x109442170
[2026-03-28 12:19:31] [CELERY] - ** ---------- .> transport:   redis://localhost:6379/0
[2026-03-28 12:19:31] [CELERY] - ** ---------- .> results:     redis://localhost:6379/0
[2026-03-28 12:19:31] [CELERY] - *** --- * --- .> concurrency: 8 (solo)
[2026-03-28 12:19:31] [CELERY] -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
[2026-03-28 12:19:31] [CELERY] --- ***** ----- 
[2026-03-28 12:19:31] [CELERY]  -------------- [queues]
[2026-03-28 12:19:31] [CELERY]                 .> celery           exchange=celery(direct) key=celery
[2026-03-28 12:19:31] [CELERY]                 
[2026-03-28 12:19:31] [CELERY] 
[2026-03-28 12:19:31] [CELERY] [tasks]
[2026-03-28 12:19:31] [CELERY]   . app.tasks.ocr_tasks.run_historical_ocr_backfill
[2026-03-28 12:19:31] [CELERY]   . app.tasks.scraping_tasks.run_scraping_task
[2026-03-28 12:19:31] [CELERY] 
[2026-03-28 12:19:31] [CELERY] 2026-03-28 12:19:31,434 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 12:19:31] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 12:19:31] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 12:19:31] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 12:19:31] [CELERY]   warnings.warn(
[2026-03-28 12:19:31] [CELERY] 
[2026-03-28 12:19:31] [CELERY] 2026-03-28 12:19:31,437 - celery.worker.consumer.connection - INFO - Connected to redis://localhost:6379/0
[2026-03-28 12:19:31] [CELERY] 2026-03-28 12:19:31,437 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 12:19:31] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 12:19:31] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 12:19:31] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 12:19:31] [CELERY]   warnings.warn(
[2026-03-28 12:19:31] [CELERY] 
[2026-03-28 12:19:31] [CELERY] 2026-03-28 12:19:31,438 - celery.worker.consumer.mingle - INFO - mingle: searching for neighbors
[2026-03-28 12:19:32] [CELERY] 2026-03-28 12:19:32,444 - celery.worker.consumer.mingle - INFO - mingle: all alone
[2026-03-28 12:19:32] [CELERY] 2026-03-28 12:19:32,451 - celery.apps.worker - INFO - celery@192.168.1.8 ready.
[2026-03-28 12:19:33] [BACKEND] [+] Remote database IP found: 172.18.0.6. Establishing tunnel...
[2026-03-28 12:19:33] [BACKEND] [+] SSH Tunnel successfully established to 172.18.0.6.
[2026-03-28 12:19:33] [BACKEND] [+] Starting FastAPI server...
[2026-03-28 12:19:40] [BACKEND] INFO:     Started server process [3433]
[2026-03-28 12:19:40] [BACKEND] INFO:     Waiting for application startup.
[2026-03-28 12:19:42] [BACKEND] INFO:     Application startup complete.
[2026-03-28 12:19:42] [BACKEND] INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
[2026-03-28 12:19:49] [FRONTEND]  ✓ Compiled /src/middleware in 81ms (73 modules)
[2026-03-28 12:19:49] [FRONTEND]  ○ Compiling /login ...
[2026-03-28 12:19:50] [FRONTEND]  ✓ Compiled /login in 1593ms (4329 modules)
[2026-03-28 12:19:50] [FRONTEND]  GET /login/?callbackUrl=%2Fdashboard%2F 200 in 1747ms
[2026-03-28 12:19:51] [FRONTEND]  ○ Compiling /manifest.webmanifest ...
[2026-03-28 12:19:51] [FRONTEND]  ✓ Compiled /manifest.webmanifest in 657ms (4365 modules)
[2026-03-28 12:19:51] [FRONTEND]  GET /manifest.webmanifest 200 in 1104ms
[2026-03-28 12:19:51] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 1106ms
[2026-03-28 12:19:55] [BACKEND] 2026-03-28 12:19:55,776 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-28 12:19:56] [FRONTEND]  ○ Compiling /admin ...
[2026-03-28 12:19:57] [FRONTEND]  ✓ Compiled /admin in 2.2s (8024 modules)
[2026-03-28 12:19:58] [BACKEND] 2026-03-28 12:19:58,180 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-28 12:19:58] [FRONTEND]  GET /manifest.webmanifest 200 in 18ms
[2026-03-28 12:19:58] [BACKEND] DEBUG: require-admin entered for turgaykirkil@me.com
[2026-03-28 12:19:58] [BACKEND] DEBUG: require-admin check: is_admin=True
[2026-03-28 12:19:58] [BACKEND] 2026-03-28 12:19:58,589 - app.api.api_v1.endpoints.auth - WARNING - [require-admin] user=turgaykirkil@me.com role=admin is_admin=True
[2026-03-28 12:19:58] [BACKEND] DEBUG: require-admin entered for turgaykirkil@me.com
[2026-03-28 12:19:58] [BACKEND] DEBUG: require-admin check: is_admin=True
[2026-03-28 12:19:58] [BACKEND] 2026-03-28 12:19:58,857 - app.api.api_v1.endpoints.auth - WARNING - [require-admin] user=turgaykirkil@me.com role=admin is_admin=True
[2026-03-28 12:20:00] [FRONTEND]  GET /dashboard/ 200 in 138ms
[2026-03-28 12:20:00] [FRONTEND]  GET /manifest.webmanifest 200 in 20ms
[2026-03-28 12:20:00] [BACKEND] 2026-03-28 12:20:00,701 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-28 12:20:00] [BACKEND] 2026-03-28 12:20:00,826 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-28 12:20:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 12:20:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 12:20:09] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 12:20:11] [FRONTEND]  GET /manifest.webmanifest 200 in 15ms
[2026-03-28 12:20:11] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 19ms
[2026-03-28 12:20:16] [FRONTEND]  ✓ Compiled /api/v1/search/company-detail in 492ms (4099 modules)
[2026-03-28 12:20:17] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 200 in 1578ms
[2026-03-28 12:20:18] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 12:21:08] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 12:22:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 12:22:49] [BACKEND] ./run_backend.sh: line 43:  3433 Killed: 9               uvicorn app.main:app --host 0.0.0.0 --port 5001
[2026-03-28 12:22:49] [BACKEND] ./run_backend.sh exited with code 137
[2026-03-28 12:23:01] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:23:01] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:23:01] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:23:01] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:23:01] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:23:01] [FRONTEND]   [errors]: [
[2026-03-28 12:23:01] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:23:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:23:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:23:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:23:01] [FRONTEND]       errno: -61,
[2026-03-28 12:23:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:23:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:23:01] [FRONTEND]       address: '::1',
[2026-03-28 12:23:01] [FRONTEND]       port: 5001
[2026-03-28 12:23:01] [FRONTEND]     },
[2026-03-28 12:23:01] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:23:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:23:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:23:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:23:01] [FRONTEND]       errno: -61,
[2026-03-28 12:23:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:23:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:23:01] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:23:01] [FRONTEND]       port: 5001
[2026-03-28 12:23:01] [FRONTEND]     }
[2026-03-28 12:23:01] [FRONTEND]   ]
[2026-03-28 12:23:01] [FRONTEND] }
[2026-03-28 12:23:01] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:23:01] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:23:01] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:23:01] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:23:01] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:23:01] [FRONTEND]   [errors]: [
[2026-03-28 12:23:01] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:23:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:23:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:23:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:23:01] [FRONTEND]       errno: -61,
[2026-03-28 12:23:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:23:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:23:01] [FRONTEND]       address: '::1',
[2026-03-28 12:23:01] [FRONTEND]       port: 5001
[2026-03-28 12:23:01] [FRONTEND]     },
[2026-03-28 12:23:01] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:23:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:23:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:23:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:23:01] [FRONTEND]       errno: -61,
[2026-03-28 12:23:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:23:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:23:01] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:23:01] [FRONTEND]       port: 5001
[2026-03-28 12:23:01] [FRONTEND]     }
[2026-03-28 12:23:01] [FRONTEND]   ]
[2026-03-28 12:23:01] [FRONTEND] }
[2026-03-28 12:23:02] [FRONTEND]  ○ Compiling /_error ...
[2026-03-28 12:23:02] [FRONTEND]  ✓ Compiled /_error in 991ms (8218 modules)
[2026-03-28 12:24:01] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:24:01] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:24:01] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:24:01] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:24:01] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:24:01] [FRONTEND]   [errors]: [
[2026-03-28 12:24:01] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:24:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:24:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:24:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:24:01] [FRONTEND]       errno: -61,
[2026-03-28 12:24:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:24:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:24:01] [FRONTEND]       address: '::1',
[2026-03-28 12:24:01] [FRONTEND]       port: 5001
[2026-03-28 12:24:01] [FRONTEND]     },
[2026-03-28 12:24:01] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:24:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:24:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:24:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:24:01] [FRONTEND]       errno: -61,
[2026-03-28 12:24:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:24:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:24:01] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:24:01] [FRONTEND]       port: 5001
[2026-03-28 12:24:01] [FRONTEND]     }
[2026-03-28 12:24:01] [FRONTEND]   ]
[2026-03-28 12:24:01] [FRONTEND] }
[2026-03-28 12:24:01] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:24:01] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:24:01] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:24:01] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:24:01] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:24:01] [FRONTEND]   [errors]: [
[2026-03-28 12:24:01] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:24:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:24:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:24:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:24:01] [FRONTEND]       errno: -61,
[2026-03-28 12:24:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:24:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:24:01] [FRONTEND]       address: '::1',
[2026-03-28 12:24:01] [FRONTEND]       port: 5001
[2026-03-28 12:24:01] [FRONTEND]     },
[2026-03-28 12:24:01] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:24:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:24:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:24:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:24:01] [FRONTEND]       errno: -61,
[2026-03-28 12:24:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:24:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:24:01] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:24:01] [FRONTEND]       port: 5001
[2026-03-28 12:24:01] [FRONTEND]     }
[2026-03-28 12:24:01] [FRONTEND]   ]
[2026-03-28 12:24:01] [FRONTEND] }
[2026-03-28 12:25:01] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:25:01] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:25:01] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:25:01] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:25:01] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:25:01] [FRONTEND]   [errors]: [
[2026-03-28 12:25:01] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:25:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:25:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:25:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:25:01] [FRONTEND]       errno: -61,
[2026-03-28 12:25:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:25:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:25:01] [FRONTEND]       address: '::1',
[2026-03-28 12:25:01] [FRONTEND]       port: 5001
[2026-03-28 12:25:01] [FRONTEND]     },
[2026-03-28 12:25:01] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:25:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:25:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:25:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:25:01] [FRONTEND]       errno: -61,
[2026-03-28 12:25:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:25:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:25:01] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:25:01] [FRONTEND]       port: 5001
[2026-03-28 12:25:01] [FRONTEND]     }
[2026-03-28 12:25:01] [FRONTEND]   ]
[2026-03-28 12:25:01] [FRONTEND] }
[2026-03-28 12:25:01] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:25:01] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:25:01] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:25:01] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:25:01] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:25:01] [FRONTEND]   [errors]: [
[2026-03-28 12:25:01] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:25:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:25:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:25:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:25:01] [FRONTEND]       errno: -61,
[2026-03-28 12:25:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:25:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:25:01] [FRONTEND]       address: '::1',
[2026-03-28 12:25:01] [FRONTEND]       port: 5001
[2026-03-28 12:25:01] [FRONTEND]     },
[2026-03-28 12:25:01] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:25:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:25:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:25:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:25:01] [FRONTEND]       errno: -61,
[2026-03-28 12:25:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:25:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:25:01] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:25:01] [FRONTEND]       port: 5001
[2026-03-28 12:25:01] [FRONTEND]     }
[2026-03-28 12:25:01] [FRONTEND]   ]
[2026-03-28 12:25:01] [FRONTEND] }
[2026-03-28 12:26:01] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:26:01] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:26:01] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:26:01] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:26:01] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:26:01] [FRONTEND]   [errors]: [
[2026-03-28 12:26:01] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:26:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:26:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:26:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:26:01] [FRONTEND]       errno: -61,
[2026-03-28 12:26:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:26:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:26:01] [FRONTEND]       address: '::1',
[2026-03-28 12:26:01] [FRONTEND]       port: 5001
[2026-03-28 12:26:01] [FRONTEND]     },
[2026-03-28 12:26:01] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:26:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:26:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:26:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:26:01] [FRONTEND]       errno: -61,
[2026-03-28 12:26:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:26:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:26:01] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:26:01] [FRONTEND]       port: 5001
[2026-03-28 12:26:01] [FRONTEND]     }
[2026-03-28 12:26:01] [FRONTEND]   ]
[2026-03-28 12:26:01] [FRONTEND] }
[2026-03-28 12:26:01] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:26:01] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:26:01] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:26:01] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:26:01] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:26:01] [FRONTEND]   [errors]: [
[2026-03-28 12:26:01] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:26:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:26:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:26:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:26:01] [FRONTEND]       errno: -61,
[2026-03-28 12:26:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:26:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:26:01] [FRONTEND]       address: '::1',
[2026-03-28 12:26:01] [FRONTEND]       port: 5001
[2026-03-28 12:26:01] [FRONTEND]     },
[2026-03-28 12:26:01] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:26:01] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:26:01] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:26:01] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:26:01] [FRONTEND]       errno: -61,
[2026-03-28 12:26:01] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:26:01] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:26:01] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:26:01] [FRONTEND]       port: 5001
[2026-03-28 12:26:01] [FRONTEND]     }
[2026-03-28 12:26:01] [FRONTEND]   ]
[2026-03-28 12:26:01] [FRONTEND] }
[2026-03-28 12:27:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:27:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:27:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:27:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:27:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:27:23] [FRONTEND]   [errors]: [
[2026-03-28 12:27:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:27:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:27:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:27:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:27:23] [FRONTEND]       errno: -61,
[2026-03-28 12:27:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:27:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:27:23] [FRONTEND]       address: '::1',
[2026-03-28 12:27:23] [FRONTEND]       port: 5001
[2026-03-28 12:27:23] [FRONTEND]     },
[2026-03-28 12:27:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:27:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:27:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:27:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:27:23] [FRONTEND]       errno: -61,
[2026-03-28 12:27:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:27:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:27:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:27:23] [FRONTEND]       port: 5001
[2026-03-28 12:27:23] [FRONTEND]     }
[2026-03-28 12:27:23] [FRONTEND]   ]
[2026-03-28 12:27:23] [FRONTEND] }
[2026-03-28 12:27:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:27:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:27:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:27:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:27:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:27:23] [FRONTEND]   [errors]: [
[2026-03-28 12:27:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:27:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:27:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:27:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:27:23] [FRONTEND]       errno: -61,
[2026-03-28 12:27:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:27:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:27:23] [FRONTEND]       address: '::1',
[2026-03-28 12:27:23] [FRONTEND]       port: 5001
[2026-03-28 12:27:23] [FRONTEND]     },
[2026-03-28 12:27:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:27:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:27:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:27:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:27:23] [FRONTEND]       errno: -61,
[2026-03-28 12:27:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:27:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:27:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:27:23] [FRONTEND]       port: 5001
[2026-03-28 12:27:23] [FRONTEND]     }
[2026-03-28 12:27:23] [FRONTEND]   ]
[2026-03-28 12:27:23] [FRONTEND] }
[2026-03-28 12:28:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:28:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:28:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:28:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:28:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:28:23] [FRONTEND]   [errors]: [
[2026-03-28 12:28:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:28:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:28:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:28:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:28:23] [FRONTEND]       errno: -61,
[2026-03-28 12:28:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:28:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:28:23] [FRONTEND]       address: '::1',
[2026-03-28 12:28:23] [FRONTEND]       port: 5001
[2026-03-28 12:28:23] [FRONTEND]     },
[2026-03-28 12:28:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:28:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:28:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:28:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:28:23] [FRONTEND]       errno: -61,
[2026-03-28 12:28:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:28:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:28:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:28:23] [FRONTEND]       port: 5001
[2026-03-28 12:28:23] [FRONTEND]     }
[2026-03-28 12:28:23] [FRONTEND]   ]
[2026-03-28 12:28:23] [FRONTEND] }
[2026-03-28 12:28:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:28:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:28:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:28:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:28:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:28:23] [FRONTEND]   [errors]: [
[2026-03-28 12:28:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:28:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:28:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:28:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:28:23] [FRONTEND]       errno: -61,
[2026-03-28 12:28:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:28:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:28:23] [FRONTEND]       address: '::1',
[2026-03-28 12:28:23] [FRONTEND]       port: 5001
[2026-03-28 12:28:23] [FRONTEND]     },
[2026-03-28 12:28:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:28:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:28:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:28:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:28:23] [FRONTEND]       errno: -61,
[2026-03-28 12:28:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:28:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:28:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:28:23] [FRONTEND]       port: 5001
[2026-03-28 12:28:23] [FRONTEND]     }
[2026-03-28 12:28:23] [FRONTEND]   ]
[2026-03-28 12:28:23] [FRONTEND] }
[2026-03-28 12:29:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:29:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:29:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:29:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:29:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:29:23] [FRONTEND]   [errors]: [
[2026-03-28 12:29:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:29:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:29:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:29:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:29:23] [FRONTEND]       errno: -61,
[2026-03-28 12:29:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:29:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:29:23] [FRONTEND]       address: '::1',
[2026-03-28 12:29:23] [FRONTEND]       port: 5001
[2026-03-28 12:29:23] [FRONTEND]     },
[2026-03-28 12:29:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:29:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:29:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:29:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:29:23] [FRONTEND]       errno: -61,
[2026-03-28 12:29:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:29:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:29:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:29:23] [FRONTEND]       port: 5001
[2026-03-28 12:29:23] [FRONTEND]     }
[2026-03-28 12:29:23] [FRONTEND]   ]
[2026-03-28 12:29:23] [FRONTEND] }
[2026-03-28 12:29:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:29:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:29:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:29:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:29:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:29:23] [FRONTEND]   [errors]: [
[2026-03-28 12:29:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:29:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:29:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:29:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:29:23] [FRONTEND]       errno: -61,
[2026-03-28 12:29:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:29:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:29:23] [FRONTEND]       address: '::1',
[2026-03-28 12:29:23] [FRONTEND]       port: 5001
[2026-03-28 12:29:23] [FRONTEND]     },
[2026-03-28 12:29:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:29:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:29:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:29:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:29:23] [FRONTEND]       errno: -61,
[2026-03-28 12:29:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:29:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:29:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:29:23] [FRONTEND]       port: 5001
[2026-03-28 12:29:23] [FRONTEND]     }
[2026-03-28 12:29:23] [FRONTEND]   ]
[2026-03-28 12:29:23] [FRONTEND] }
[2026-03-28 12:30:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:30:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:30:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:30:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:30:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:30:23] [FRONTEND]   [errors]: [
[2026-03-28 12:30:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:30:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:30:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:30:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:30:23] [FRONTEND]       errno: -61,
[2026-03-28 12:30:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:30:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:30:23] [FRONTEND]       address: '::1',
[2026-03-28 12:30:23] [FRONTEND]       port: 5001
[2026-03-28 12:30:23] [FRONTEND]     },
[2026-03-28 12:30:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:30:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:30:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:30:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:30:23] [FRONTEND]       errno: -61,
[2026-03-28 12:30:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:30:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:30:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:30:23] [FRONTEND]       port: 5001
[2026-03-28 12:30:23] [FRONTEND]     }
[2026-03-28 12:30:23] [FRONTEND]   ]
[2026-03-28 12:30:23] [FRONTEND] }
[2026-03-28 12:30:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:30:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:30:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:30:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:30:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:30:23] [FRONTEND]   [errors]: [
[2026-03-28 12:30:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:30:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:30:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:30:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:30:23] [FRONTEND]       errno: -61,
[2026-03-28 12:30:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:30:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:30:23] [FRONTEND]       address: '::1',
[2026-03-28 12:30:23] [FRONTEND]       port: 5001
[2026-03-28 12:30:23] [FRONTEND]     },
[2026-03-28 12:30:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:30:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:30:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:30:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:30:23] [FRONTEND]       errno: -61,
[2026-03-28 12:30:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:30:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:30:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:30:23] [FRONTEND]       port: 5001
[2026-03-28 12:30:23] [FRONTEND]     }
[2026-03-28 12:30:23] [FRONTEND]   ]
[2026-03-28 12:30:23] [FRONTEND] }
[2026-03-28 12:31:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:31:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:31:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:31:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:31:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:31:23] [FRONTEND]   [errors]: [
[2026-03-28 12:31:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:31:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:31:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:31:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:31:23] [FRONTEND]       errno: -61,
[2026-03-28 12:31:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:31:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:31:23] [FRONTEND]       address: '::1',
[2026-03-28 12:31:23] [FRONTEND]       port: 5001
[2026-03-28 12:31:23] [FRONTEND]     },
[2026-03-28 12:31:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:31:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:31:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:31:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:31:23] [FRONTEND]       errno: -61,
[2026-03-28 12:31:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:31:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:31:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:31:23] [FRONTEND]       port: 5001
[2026-03-28 12:31:23] [FRONTEND]     }
[2026-03-28 12:31:23] [FRONTEND]   ]
[2026-03-28 12:31:23] [FRONTEND] }
[2026-03-28 12:31:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:31:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:31:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:31:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:31:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:31:23] [FRONTEND]   [errors]: [
[2026-03-28 12:31:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:31:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:31:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:31:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:31:23] [FRONTEND]       errno: -61,
[2026-03-28 12:31:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:31:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:31:23] [FRONTEND]       address: '::1',
[2026-03-28 12:31:23] [FRONTEND]       port: 5001
[2026-03-28 12:31:23] [FRONTEND]     },
[2026-03-28 12:31:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:31:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:31:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:31:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:31:23] [FRONTEND]       errno: -61,
[2026-03-28 12:31:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:31:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:31:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:31:23] [FRONTEND]       port: 5001
[2026-03-28 12:31:23] [FRONTEND]     }
[2026-03-28 12:31:23] [FRONTEND]   ]
[2026-03-28 12:31:23] [FRONTEND] }
[2026-03-28 12:32:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:32:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:32:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:32:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:32:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:32:23] [FRONTEND]   [errors]: [
[2026-03-28 12:32:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:32:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:32:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:32:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:32:23] [FRONTEND]       errno: -61,
[2026-03-28 12:32:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:32:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:32:23] [FRONTEND]       address: '::1',
[2026-03-28 12:32:23] [FRONTEND]       port: 5001
[2026-03-28 12:32:23] [FRONTEND]     },
[2026-03-28 12:32:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:32:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:32:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:32:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:32:23] [FRONTEND]       errno: -61,
[2026-03-28 12:32:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:32:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:32:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:32:23] [FRONTEND]       port: 5001
[2026-03-28 12:32:23] [FRONTEND]     }
[2026-03-28 12:32:23] [FRONTEND]   ]
[2026-03-28 12:32:23] [FRONTEND] }
[2026-03-28 12:32:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:32:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:32:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:32:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:32:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:32:23] [FRONTEND]   [errors]: [
[2026-03-28 12:32:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:32:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:32:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:32:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:32:23] [FRONTEND]       errno: -61,
[2026-03-28 12:32:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:32:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:32:23] [FRONTEND]       address: '::1',
[2026-03-28 12:32:23] [FRONTEND]       port: 5001
[2026-03-28 12:32:23] [FRONTEND]     },
[2026-03-28 12:32:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:32:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:32:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:32:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:32:23] [FRONTEND]       errno: -61,
[2026-03-28 12:32:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:32:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:32:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:32:23] [FRONTEND]       port: 5001
[2026-03-28 12:32:23] [FRONTEND]     }
[2026-03-28 12:32:23] [FRONTEND]   ]
[2026-03-28 12:32:23] [FRONTEND] }
[2026-03-28 12:33:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:33:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:33:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:33:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:33:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:33:23] [FRONTEND]   [errors]: [
[2026-03-28 12:33:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:33:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:33:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:33:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:33:23] [FRONTEND]       errno: -61,
[2026-03-28 12:33:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:33:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:33:23] [FRONTEND]       address: '::1',
[2026-03-28 12:33:23] [FRONTEND]       port: 5001
[2026-03-28 12:33:23] [FRONTEND]     },
[2026-03-28 12:33:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:33:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:33:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:33:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:33:23] [FRONTEND]       errno: -61,
[2026-03-28 12:33:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:33:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:33:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:33:23] [FRONTEND]       port: 5001
[2026-03-28 12:33:23] [FRONTEND]     }
[2026-03-28 12:33:23] [FRONTEND]   ]
[2026-03-28 12:33:23] [FRONTEND] }
[2026-03-28 12:33:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:33:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:33:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:33:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:33:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:33:23] [FRONTEND]   [errors]: [
[2026-03-28 12:33:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:33:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:33:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:33:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:33:23] [FRONTEND]       errno: -61,
[2026-03-28 12:33:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:33:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:33:23] [FRONTEND]       address: '::1',
[2026-03-28 12:33:23] [FRONTEND]       port: 5001
[2026-03-28 12:33:23] [FRONTEND]     },
[2026-03-28 12:33:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:33:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:33:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:33:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:33:23] [FRONTEND]       errno: -61,
[2026-03-28 12:33:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:33:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:33:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:33:23] [FRONTEND]       port: 5001
[2026-03-28 12:33:23] [FRONTEND]     }
[2026-03-28 12:33:23] [FRONTEND]   ]
[2026-03-28 12:33:23] [FRONTEND] }
[2026-03-28 12:34:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:34:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:34:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:34:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:34:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:34:23] [FRONTEND]   [errors]: [
[2026-03-28 12:34:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:34:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:34:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:34:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:34:23] [FRONTEND]       errno: -61,
[2026-03-28 12:34:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:34:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:34:23] [FRONTEND]       address: '::1',
[2026-03-28 12:34:23] [FRONTEND]       port: 5001
[2026-03-28 12:34:23] [FRONTEND]     },
[2026-03-28 12:34:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:34:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:34:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:34:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:34:23] [FRONTEND]       errno: -61,
[2026-03-28 12:34:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:34:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:34:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:34:23] [FRONTEND]       port: 5001
[2026-03-28 12:34:23] [FRONTEND]     }
[2026-03-28 12:34:23] [FRONTEND]   ]
[2026-03-28 12:34:23] [FRONTEND] }
[2026-03-28 12:34:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:34:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:34:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:34:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:34:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:34:23] [FRONTEND]   [errors]: [
[2026-03-28 12:34:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:34:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:34:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:34:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:34:23] [FRONTEND]       errno: -61,
[2026-03-28 12:34:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:34:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:34:23] [FRONTEND]       address: '::1',
[2026-03-28 12:34:23] [FRONTEND]       port: 5001
[2026-03-28 12:34:23] [FRONTEND]     },
[2026-03-28 12:34:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:34:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:34:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:34:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:34:23] [FRONTEND]       errno: -61,
[2026-03-28 12:34:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:34:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:34:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:34:23] [FRONTEND]       port: 5001
[2026-03-28 12:34:23] [FRONTEND]     }
[2026-03-28 12:34:23] [FRONTEND]   ]
[2026-03-28 12:34:23] [FRONTEND] }
[2026-03-28 12:35:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:35:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:35:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:35:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:35:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:35:23] [FRONTEND]   [errors]: [
[2026-03-28 12:35:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:35:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:35:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:35:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:35:23] [FRONTEND]       errno: -61,
[2026-03-28 12:35:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:35:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:35:23] [FRONTEND]       address: '::1',
[2026-03-28 12:35:23] [FRONTEND]       port: 5001
[2026-03-28 12:35:23] [FRONTEND]     },
[2026-03-28 12:35:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:35:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:35:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:35:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:35:23] [FRONTEND]       errno: -61,
[2026-03-28 12:35:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:35:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:35:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:35:23] [FRONTEND]       port: 5001
[2026-03-28 12:35:23] [FRONTEND]     }
[2026-03-28 12:35:23] [FRONTEND]   ]
[2026-03-28 12:35:23] [FRONTEND] }
[2026-03-28 12:35:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:35:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:35:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:35:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:35:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:35:23] [FRONTEND]   [errors]: [
[2026-03-28 12:35:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:35:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:35:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:35:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:35:23] [FRONTEND]       errno: -61,
[2026-03-28 12:35:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:35:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:35:23] [FRONTEND]       address: '::1',
[2026-03-28 12:35:23] [FRONTEND]       port: 5001
[2026-03-28 12:35:23] [FRONTEND]     },
[2026-03-28 12:35:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:35:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:35:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:35:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:35:23] [FRONTEND]       errno: -61,
[2026-03-28 12:35:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:35:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:35:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:35:23] [FRONTEND]       port: 5001
[2026-03-28 12:35:23] [FRONTEND]     }
[2026-03-28 12:35:23] [FRONTEND]   ]
[2026-03-28 12:35:23] [FRONTEND] }
[2026-03-28 12:36:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:36:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:36:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:36:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:36:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:36:23] [FRONTEND]   [errors]: [
[2026-03-28 12:36:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:36:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:36:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:36:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:36:23] [FRONTEND]       errno: -61,
[2026-03-28 12:36:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:36:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:36:23] [FRONTEND]       address: '::1',
[2026-03-28 12:36:23] [FRONTEND]       port: 5001
[2026-03-28 12:36:23] [FRONTEND]     },
[2026-03-28 12:36:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:36:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:36:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:36:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:36:23] [FRONTEND]       errno: -61,
[2026-03-28 12:36:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:36:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:36:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:36:23] [FRONTEND]       port: 5001
[2026-03-28 12:36:23] [FRONTEND]     }
[2026-03-28 12:36:23] [FRONTEND]   ]
[2026-03-28 12:36:23] [FRONTEND] }
[2026-03-28 12:36:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:36:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:36:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:36:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:36:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:36:23] [FRONTEND]   [errors]: [
[2026-03-28 12:36:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:36:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:36:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:36:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:36:23] [FRONTEND]       errno: -61,
[2026-03-28 12:36:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:36:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:36:23] [FRONTEND]       address: '::1',
[2026-03-28 12:36:23] [FRONTEND]       port: 5001
[2026-03-28 12:36:23] [FRONTEND]     },
[2026-03-28 12:36:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:36:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:36:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:36:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:36:23] [FRONTEND]       errno: -61,
[2026-03-28 12:36:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:36:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:36:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:36:23] [FRONTEND]       port: 5001
[2026-03-28 12:36:23] [FRONTEND]     }
[2026-03-28 12:36:23] [FRONTEND]   ]
[2026-03-28 12:36:23] [FRONTEND] }
[2026-03-28 12:37:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:37:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:37:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:37:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:37:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:37:23] [FRONTEND]   [errors]: [
[2026-03-28 12:37:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:37:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:37:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:37:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:37:23] [FRONTEND]       errno: -61,
[2026-03-28 12:37:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:37:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:37:23] [FRONTEND]       address: '::1',
[2026-03-28 12:37:23] [FRONTEND]       port: 5001
[2026-03-28 12:37:23] [FRONTEND]     },
[2026-03-28 12:37:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:37:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:37:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:37:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:37:23] [FRONTEND]       errno: -61,
[2026-03-28 12:37:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:37:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:37:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:37:23] [FRONTEND]       port: 5001
[2026-03-28 12:37:23] [FRONTEND]     }
[2026-03-28 12:37:23] [FRONTEND]   ]
[2026-03-28 12:37:23] [FRONTEND] }
[2026-03-28 12:37:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:37:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:37:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:37:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:37:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:37:23] [FRONTEND]   [errors]: [
[2026-03-28 12:37:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:37:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:37:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:37:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:37:23] [FRONTEND]       errno: -61,
[2026-03-28 12:37:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:37:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:37:23] [FRONTEND]       address: '::1',
[2026-03-28 12:37:23] [FRONTEND]       port: 5001
[2026-03-28 12:37:23] [FRONTEND]     },
[2026-03-28 12:37:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:37:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:37:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:37:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:37:23] [FRONTEND]       errno: -61,
[2026-03-28 12:37:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:37:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:37:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:37:23] [FRONTEND]       port: 5001
[2026-03-28 12:37:23] [FRONTEND]     }
[2026-03-28 12:37:23] [FRONTEND]   ]
[2026-03-28 12:37:23] [FRONTEND] }
[2026-03-28 12:38:12] [FRONTEND] Browserslist: browsers data (caniuse-lite) is 9 months old. Please run:
[2026-03-28 12:38:12] [FRONTEND]   npx update-browserslist-db@latest
[2026-03-28 12:38:12] [FRONTEND]   Why you should do it regularly: https://github.com/browserslist/update-db#readme
[2026-03-28 12:38:13] [FRONTEND]  ✓ Compiled in 2.3s (8232 modules)
[2026-03-28 12:38:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/search/announcement-detail?announcement_id=9193f72a-a580-48a0-a0f8-233542afc988 AggregateError [ECONNREFUSED]: 
[2026-03-28 12:38:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:38:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:38:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]   [errors]: [
[2026-03-28 12:38:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]       errno: -61,
[2026-03-28 12:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:38:13] [FRONTEND]       address: '::1',
[2026-03-28 12:38:13] [FRONTEND]       port: 5001
[2026-03-28 12:38:13] [FRONTEND]     },
[2026-03-28 12:38:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]       errno: -61,
[2026-03-28 12:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:38:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:38:13] [FRONTEND]       port: 5001
[2026-03-28 12:38:13] [FRONTEND]     }
[2026-03-28 12:38:13] [FRONTEND]   ]
[2026-03-28 12:38:13] [FRONTEND] }
[2026-03-28 12:38:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:38:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:38:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:38:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]   [errors]: [
[2026-03-28 12:38:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]       errno: -61,
[2026-03-28 12:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:38:13] [FRONTEND]       address: '::1',
[2026-03-28 12:38:13] [FRONTEND]       port: 5001
[2026-03-28 12:38:13] [FRONTEND]     },
[2026-03-28 12:38:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]       errno: -61,
[2026-03-28 12:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:38:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:38:13] [FRONTEND]       port: 5001
[2026-03-28 12:38:13] [FRONTEND]     }
[2026-03-28 12:38:13] [FRONTEND]   ]
[2026-03-28 12:38:13] [FRONTEND] }
[2026-03-28 12:38:13] [FRONTEND]  ✓ Compiled /api/v1/search/company-detail in 194ms (4108 modules)
[2026-03-28 12:38:13] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 502 in 255ms
[2026-03-28 12:38:13] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:38:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:38:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:38:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]   [errors]: [
[2026-03-28 12:38:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]       errno: -61,
[2026-03-28 12:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:38:13] [FRONTEND]       address: '::1',
[2026-03-28 12:38:13] [FRONTEND]       port: 5001
[2026-03-28 12:38:13] [FRONTEND]     },
[2026-03-28 12:38:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]       errno: -61,
[2026-03-28 12:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:38:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:38:13] [FRONTEND]       port: 5001
[2026-03-28 12:38:13] [FRONTEND]     }
[2026-03-28 12:38:13] [FRONTEND]   ]
[2026-03-28 12:38:13] [FRONTEND] }
[2026-03-28 12:38:13] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:38:13] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:38:13] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:38:13] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]   [errors]: [
[2026-03-28 12:38:13] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]       errno: -61,
[2026-03-28 12:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:38:13] [FRONTEND]       address: '::1',
[2026-03-28 12:38:13] [FRONTEND]       port: 5001
[2026-03-28 12:38:13] [FRONTEND]     },
[2026-03-28 12:38:13] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:38:13] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:38:13] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:38:13] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:38:13] [FRONTEND]       errno: -61,
[2026-03-28 12:38:13] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:38:13] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:38:13] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:38:13] [FRONTEND]       port: 5001
[2026-03-28 12:38:13] [FRONTEND]     }
[2026-03-28 12:38:13] [FRONTEND]   ]
[2026-03-28 12:38:13] [FRONTEND] }
[2026-03-28 12:38:26] [FRONTEND]  ✓ Compiled in 1009ms (8262 modules)
[2026-03-28 12:39:14] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:39:14] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:39:14] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:39:14] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:39:14] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:39:14] [FRONTEND]   [errors]: [
[2026-03-28 12:39:14] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:39:14] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:39:14] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:39:14] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:39:14] [FRONTEND]       errno: -61,
[2026-03-28 12:39:14] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:39:14] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:39:14] [FRONTEND]       address: '::1',
[2026-03-28 12:39:14] [FRONTEND]       port: 5001
[2026-03-28 12:39:14] [FRONTEND]     },
[2026-03-28 12:39:14] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:39:14] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:39:14] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:39:14] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:39:14] [FRONTEND]       errno: -61,
[2026-03-28 12:39:14] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:39:14] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:39:14] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:39:14] [FRONTEND]       port: 5001
[2026-03-28 12:39:14] [FRONTEND]     }
[2026-03-28 12:39:14] [FRONTEND]   ]
[2026-03-28 12:39:14] [FRONTEND] }
[2026-03-28 12:39:14] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:39:14] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:39:14] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:39:14] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:39:14] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:39:14] [FRONTEND]   [errors]: [
[2026-03-28 12:39:14] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:39:14] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:39:14] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:39:14] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:39:14] [FRONTEND]       errno: -61,
[2026-03-28 12:39:14] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:39:14] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:39:14] [FRONTEND]       address: '::1',
[2026-03-28 12:39:14] [FRONTEND]       port: 5001
[2026-03-28 12:39:14] [FRONTEND]     },
[2026-03-28 12:39:14] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:39:14] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:39:14] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:39:14] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:39:14] [FRONTEND]       errno: -61,
[2026-03-28 12:39:14] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:39:14] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:39:14] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:39:14] [FRONTEND]       port: 5001
[2026-03-28 12:39:14] [FRONTEND]     }
[2026-03-28 12:39:14] [FRONTEND]   ]
[2026-03-28 12:39:14] [FRONTEND] }
[2026-03-28 12:40:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:40:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:40:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:40:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:40:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:40:23] [FRONTEND]   [errors]: [
[2026-03-28 12:40:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:40:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:40:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:40:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:40:23] [FRONTEND]       errno: -61,
[2026-03-28 12:40:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:40:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:40:23] [FRONTEND]       address: '::1',
[2026-03-28 12:40:23] [FRONTEND]       port: 5001
[2026-03-28 12:40:23] [FRONTEND]     },
[2026-03-28 12:40:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:40:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:40:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:40:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:40:23] [FRONTEND]       errno: -61,
[2026-03-28 12:40:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:40:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:40:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:40:23] [FRONTEND]       port: 5001
[2026-03-28 12:40:23] [FRONTEND]     }
[2026-03-28 12:40:23] [FRONTEND]   ]
[2026-03-28 12:40:23] [FRONTEND] }
[2026-03-28 12:40:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:40:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:40:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:40:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:40:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:40:23] [FRONTEND]   [errors]: [
[2026-03-28 12:40:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:40:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:40:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:40:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:40:23] [FRONTEND]       errno: -61,
[2026-03-28 12:40:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:40:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:40:23] [FRONTEND]       address: '::1',
[2026-03-28 12:40:23] [FRONTEND]       port: 5001
[2026-03-28 12:40:23] [FRONTEND]     },
[2026-03-28 12:40:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:40:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:40:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:40:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:40:23] [FRONTEND]       errno: -61,
[2026-03-28 12:40:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:40:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:40:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:40:23] [FRONTEND]       port: 5001
[2026-03-28 12:40:23] [FRONTEND]     }
[2026-03-28 12:40:23] [FRONTEND]   ]
[2026-03-28 12:40:23] [FRONTEND] }
[2026-03-28 12:41:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:41:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:41:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:41:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:41:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:41:23] [FRONTEND]   [errors]: [
[2026-03-28 12:41:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:41:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:41:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:41:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:41:23] [FRONTEND]       errno: -61,
[2026-03-28 12:41:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:41:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:41:23] [FRONTEND]       address: '::1',
[2026-03-28 12:41:23] [FRONTEND]       port: 5001
[2026-03-28 12:41:23] [FRONTEND]     },
[2026-03-28 12:41:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:41:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:41:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:41:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:41:23] [FRONTEND]       errno: -61,
[2026-03-28 12:41:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:41:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:41:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:41:23] [FRONTEND]       port: 5001
[2026-03-28 12:41:23] [FRONTEND]     }
[2026-03-28 12:41:23] [FRONTEND]   ]
[2026-03-28 12:41:23] [FRONTEND] }
[2026-03-28 12:41:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:41:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:41:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:41:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:41:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:41:23] [FRONTEND]   [errors]: [
[2026-03-28 12:41:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:41:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:41:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:41:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:41:23] [FRONTEND]       errno: -61,
[2026-03-28 12:41:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:41:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:41:23] [FRONTEND]       address: '::1',
[2026-03-28 12:41:23] [FRONTEND]       port: 5001
[2026-03-28 12:41:23] [FRONTEND]     },
[2026-03-28 12:41:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:41:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:41:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:41:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:41:23] [FRONTEND]       errno: -61,
[2026-03-28 12:41:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:41:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:41:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:41:23] [FRONTEND]       port: 5001
[2026-03-28 12:41:23] [FRONTEND]     }
[2026-03-28 12:41:23] [FRONTEND]   ]
[2026-03-28 12:41:23] [FRONTEND] }
[2026-03-28 12:42:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:42:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:42:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:42:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:42:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:42:23] [FRONTEND]   [errors]: [
[2026-03-28 12:42:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:42:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:42:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:42:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:42:23] [FRONTEND]       errno: -61,
[2026-03-28 12:42:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:42:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:42:23] [FRONTEND]       address: '::1',
[2026-03-28 12:42:23] [FRONTEND]       port: 5001
[2026-03-28 12:42:23] [FRONTEND]     },
[2026-03-28 12:42:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:42:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:42:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:42:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:42:23] [FRONTEND]       errno: -61,
[2026-03-28 12:42:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:42:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:42:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:42:23] [FRONTEND]       port: 5001
[2026-03-28 12:42:23] [FRONTEND]     }
[2026-03-28 12:42:23] [FRONTEND]   ]
[2026-03-28 12:42:23] [FRONTEND] }
[2026-03-28 12:42:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:42:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:42:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:42:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:42:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:42:23] [FRONTEND]   [errors]: [
[2026-03-28 12:42:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:42:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:42:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:42:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:42:23] [FRONTEND]       errno: -61,
[2026-03-28 12:42:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:42:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:42:23] [FRONTEND]       address: '::1',
[2026-03-28 12:42:23] [FRONTEND]       port: 5001
[2026-03-28 12:42:23] [FRONTEND]     },
[2026-03-28 12:42:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:42:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:42:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:42:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:42:23] [FRONTEND]       errno: -61,
[2026-03-28 12:42:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:42:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:42:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:42:23] [FRONTEND]       port: 5001
[2026-03-28 12:42:23] [FRONTEND]     }
[2026-03-28 12:42:23] [FRONTEND]   ]
[2026-03-28 12:42:23] [FRONTEND] }
[2026-03-28 12:43:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:43:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:43:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:43:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:43:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:43:23] [FRONTEND]   [errors]: [
[2026-03-28 12:43:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:43:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:43:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:43:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:43:23] [FRONTEND]       errno: -61,
[2026-03-28 12:43:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:43:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:43:23] [FRONTEND]       address: '::1',
[2026-03-28 12:43:23] [FRONTEND]       port: 5001
[2026-03-28 12:43:23] [FRONTEND]     },
[2026-03-28 12:43:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:43:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:43:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:43:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:43:23] [FRONTEND]       errno: -61,
[2026-03-28 12:43:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:43:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:43:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:43:23] [FRONTEND]       port: 5001
[2026-03-28 12:43:23] [FRONTEND]     }
[2026-03-28 12:43:23] [FRONTEND]   ]
[2026-03-28 12:43:23] [FRONTEND] }
[2026-03-28 12:43:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:43:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:43:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:43:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:43:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:43:23] [FRONTEND]   [errors]: [
[2026-03-28 12:43:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:43:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:43:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:43:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:43:23] [FRONTEND]       errno: -61,
[2026-03-28 12:43:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:43:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:43:23] [FRONTEND]       address: '::1',
[2026-03-28 12:43:23] [FRONTEND]       port: 5001
[2026-03-28 12:43:23] [FRONTEND]     },
[2026-03-28 12:43:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:43:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:43:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:43:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:43:23] [FRONTEND]       errno: -61,
[2026-03-28 12:43:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:43:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:43:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:43:23] [FRONTEND]       port: 5001
[2026-03-28 12:43:23] [FRONTEND]     }
[2026-03-28 12:43:23] [FRONTEND]   ]
[2026-03-28 12:43:23] [FRONTEND] }
[2026-03-28 12:44:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:44:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:44:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:44:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:44:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:44:23] [FRONTEND]   [errors]: [
[2026-03-28 12:44:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:44:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:44:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:44:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:44:23] [FRONTEND]       errno: -61,
[2026-03-28 12:44:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:44:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:44:23] [FRONTEND]       address: '::1',
[2026-03-28 12:44:23] [FRONTEND]       port: 5001
[2026-03-28 12:44:23] [FRONTEND]     },
[2026-03-28 12:44:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:44:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:44:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:44:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:44:23] [FRONTEND]       errno: -61,
[2026-03-28 12:44:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:44:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:44:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:44:23] [FRONTEND]       port: 5001
[2026-03-28 12:44:23] [FRONTEND]     }
[2026-03-28 12:44:23] [FRONTEND]   ]
[2026-03-28 12:44:23] [FRONTEND] }
[2026-03-28 12:44:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:44:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:44:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:44:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:44:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:44:23] [FRONTEND]   [errors]: [
[2026-03-28 12:44:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:44:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:44:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:44:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:44:23] [FRONTEND]       errno: -61,
[2026-03-28 12:44:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:44:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:44:23] [FRONTEND]       address: '::1',
[2026-03-28 12:44:23] [FRONTEND]       port: 5001
[2026-03-28 12:44:23] [FRONTEND]     },
[2026-03-28 12:44:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:44:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:44:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:44:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:44:23] [FRONTEND]       errno: -61,
[2026-03-28 12:44:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:44:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:44:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:44:23] [FRONTEND]       port: 5001
[2026-03-28 12:44:23] [FRONTEND]     }
[2026-03-28 12:44:23] [FRONTEND]   ]
[2026-03-28 12:44:23] [FRONTEND] }
[2026-03-28 12:45:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:45:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:45:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:45:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:45:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:45:23] [FRONTEND]   [errors]: [
[2026-03-28 12:45:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:45:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:45:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:45:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:45:23] [FRONTEND]       errno: -61,
[2026-03-28 12:45:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:45:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:45:23] [FRONTEND]       address: '::1',
[2026-03-28 12:45:23] [FRONTEND]       port: 5001
[2026-03-28 12:45:23] [FRONTEND]     },
[2026-03-28 12:45:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:45:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:45:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:45:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:45:23] [FRONTEND]       errno: -61,
[2026-03-28 12:45:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:45:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:45:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:45:23] [FRONTEND]       port: 5001
[2026-03-28 12:45:23] [FRONTEND]     }
[2026-03-28 12:45:23] [FRONTEND]   ]
[2026-03-28 12:45:23] [FRONTEND] }
[2026-03-28 12:45:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:45:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:45:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:45:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:45:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:45:23] [FRONTEND]   [errors]: [
[2026-03-28 12:45:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:45:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:45:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:45:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:45:23] [FRONTEND]       errno: -61,
[2026-03-28 12:45:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:45:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:45:23] [FRONTEND]       address: '::1',
[2026-03-28 12:45:23] [FRONTEND]       port: 5001
[2026-03-28 12:45:23] [FRONTEND]     },
[2026-03-28 12:45:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:45:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:45:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:45:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:45:23] [FRONTEND]       errno: -61,
[2026-03-28 12:45:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:45:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:45:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:45:23] [FRONTEND]       port: 5001
[2026-03-28 12:45:23] [FRONTEND]     }
[2026-03-28 12:45:23] [FRONTEND]   ]
[2026-03-28 12:45:23] [FRONTEND] }
[2026-03-28 12:46:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:46:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:46:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:46:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:46:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:46:23] [FRONTEND]   [errors]: [
[2026-03-28 12:46:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:46:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:46:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:46:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:46:23] [FRONTEND]       errno: -61,
[2026-03-28 12:46:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:46:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:46:23] [FRONTEND]       address: '::1',
[2026-03-28 12:46:23] [FRONTEND]       port: 5001
[2026-03-28 12:46:23] [FRONTEND]     },
[2026-03-28 12:46:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:46:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:46:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:46:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:46:23] [FRONTEND]       errno: -61,
[2026-03-28 12:46:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:46:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:46:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:46:23] [FRONTEND]       port: 5001
[2026-03-28 12:46:23] [FRONTEND]     }
[2026-03-28 12:46:23] [FRONTEND]   ]
[2026-03-28 12:46:23] [FRONTEND] }
[2026-03-28 12:46:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:46:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:46:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:46:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:46:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:46:23] [FRONTEND]   [errors]: [
[2026-03-28 12:46:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:46:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:46:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:46:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:46:23] [FRONTEND]       errno: -61,
[2026-03-28 12:46:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:46:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:46:23] [FRONTEND]       address: '::1',
[2026-03-28 12:46:23] [FRONTEND]       port: 5001
[2026-03-28 12:46:23] [FRONTEND]     },
[2026-03-28 12:46:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:46:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:46:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:46:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:46:23] [FRONTEND]       errno: -61,
[2026-03-28 12:46:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:46:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:46:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:46:23] [FRONTEND]       port: 5001
[2026-03-28 12:46:23] [FRONTEND]     }
[2026-03-28 12:46:23] [FRONTEND]   ]
[2026-03-28 12:46:23] [FRONTEND] }
[2026-03-28 12:47:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:47:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:47:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:47:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:47:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:47:23] [FRONTEND]   [errors]: [
[2026-03-28 12:47:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:47:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:47:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:47:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:47:23] [FRONTEND]       errno: -61,
[2026-03-28 12:47:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:47:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:47:23] [FRONTEND]       address: '::1',
[2026-03-28 12:47:23] [FRONTEND]       port: 5001
[2026-03-28 12:47:23] [FRONTEND]     },
[2026-03-28 12:47:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:47:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:47:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:47:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:47:23] [FRONTEND]       errno: -61,
[2026-03-28 12:47:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:47:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:47:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:47:23] [FRONTEND]       port: 5001
[2026-03-28 12:47:23] [FRONTEND]     }
[2026-03-28 12:47:23] [FRONTEND]   ]
[2026-03-28 12:47:23] [FRONTEND] }
[2026-03-28 12:47:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:47:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:47:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:47:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:47:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:47:23] [FRONTEND]   [errors]: [
[2026-03-28 12:47:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:47:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:47:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:47:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:47:23] [FRONTEND]       errno: -61,
[2026-03-28 12:47:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:47:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:47:23] [FRONTEND]       address: '::1',
[2026-03-28 12:47:23] [FRONTEND]       port: 5001
[2026-03-28 12:47:23] [FRONTEND]     },
[2026-03-28 12:47:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:47:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:47:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:47:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:47:23] [FRONTEND]       errno: -61,
[2026-03-28 12:47:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:47:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:47:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:47:23] [FRONTEND]       port: 5001
[2026-03-28 12:47:23] [FRONTEND]     }
[2026-03-28 12:47:23] [FRONTEND]   ]
[2026-03-28 12:47:23] [FRONTEND] }
[2026-03-28 12:48:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:48:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:48:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:48:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:48:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:48:23] [FRONTEND]   [errors]: [
[2026-03-28 12:48:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:48:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:48:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:48:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:48:23] [FRONTEND]       errno: -61,
[2026-03-28 12:48:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:48:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:48:23] [FRONTEND]       address: '::1',
[2026-03-28 12:48:23] [FRONTEND]       port: 5001
[2026-03-28 12:48:23] [FRONTEND]     },
[2026-03-28 12:48:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:48:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:48:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:48:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:48:23] [FRONTEND]       errno: -61,
[2026-03-28 12:48:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:48:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:48:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:48:23] [FRONTEND]       port: 5001
[2026-03-28 12:48:23] [FRONTEND]     }
[2026-03-28 12:48:23] [FRONTEND]   ]
[2026-03-28 12:48:23] [FRONTEND] }
[2026-03-28 12:48:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:48:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:48:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:48:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:48:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:48:23] [FRONTEND]   [errors]: [
[2026-03-28 12:48:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:48:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:48:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:48:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:48:23] [FRONTEND]       errno: -61,
[2026-03-28 12:48:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:48:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:48:23] [FRONTEND]       address: '::1',
[2026-03-28 12:48:23] [FRONTEND]       port: 5001
[2026-03-28 12:48:23] [FRONTEND]     },
[2026-03-28 12:48:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:48:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:48:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:48:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:48:23] [FRONTEND]       errno: -61,
[2026-03-28 12:48:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:48:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:48:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:48:23] [FRONTEND]       port: 5001
[2026-03-28 12:48:23] [FRONTEND]     }
[2026-03-28 12:48:23] [FRONTEND]   ]
[2026-03-28 12:48:23] [FRONTEND] }
[2026-03-28 12:49:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:49:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:49:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:49:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:49:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:49:23] [FRONTEND]   [errors]: [
[2026-03-28 12:49:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:49:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:49:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:49:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:49:23] [FRONTEND]       errno: -61,
[2026-03-28 12:49:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:49:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:49:23] [FRONTEND]       address: '::1',
[2026-03-28 12:49:23] [FRONTEND]       port: 5001
[2026-03-28 12:49:23] [FRONTEND]     },
[2026-03-28 12:49:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:49:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:49:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:49:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:49:23] [FRONTEND]       errno: -61,
[2026-03-28 12:49:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:49:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:49:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:49:23] [FRONTEND]       port: 5001
[2026-03-28 12:49:23] [FRONTEND]     }
[2026-03-28 12:49:23] [FRONTEND]   ]
[2026-03-28 12:49:23] [FRONTEND] }
[2026-03-28 12:49:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:49:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:49:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:49:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:49:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:49:23] [FRONTEND]   [errors]: [
[2026-03-28 12:49:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:49:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:49:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:49:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:49:23] [FRONTEND]       errno: -61,
[2026-03-28 12:49:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:49:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:49:23] [FRONTEND]       address: '::1',
[2026-03-28 12:49:23] [FRONTEND]       port: 5001
[2026-03-28 12:49:23] [FRONTEND]     },
[2026-03-28 12:49:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:49:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:49:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:49:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:49:23] [FRONTEND]       errno: -61,
[2026-03-28 12:49:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:49:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:49:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:49:23] [FRONTEND]       port: 5001
[2026-03-28 12:49:23] [FRONTEND]     }
[2026-03-28 12:49:23] [FRONTEND]   ]
[2026-03-28 12:49:23] [FRONTEND] }
[2026-03-28 12:50:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:50:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:50:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:50:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:50:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:50:23] [FRONTEND]   [errors]: [
[2026-03-28 12:50:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:50:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:50:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:50:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:50:23] [FRONTEND]       errno: -61,
[2026-03-28 12:50:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:50:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:50:23] [FRONTEND]       address: '::1',
[2026-03-28 12:50:23] [FRONTEND]       port: 5001
[2026-03-28 12:50:23] [FRONTEND]     },
[2026-03-28 12:50:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:50:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:50:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:50:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:50:23] [FRONTEND]       errno: -61,
[2026-03-28 12:50:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:50:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:50:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:50:23] [FRONTEND]       port: 5001
[2026-03-28 12:50:23] [FRONTEND]     }
[2026-03-28 12:50:23] [FRONTEND]   ]
[2026-03-28 12:50:23] [FRONTEND] }
[2026-03-28 12:50:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:50:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:50:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:50:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:50:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:50:23] [FRONTEND]   [errors]: [
[2026-03-28 12:50:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:50:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:50:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:50:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:50:23] [FRONTEND]       errno: -61,
[2026-03-28 12:50:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:50:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:50:23] [FRONTEND]       address: '::1',
[2026-03-28 12:50:23] [FRONTEND]       port: 5001
[2026-03-28 12:50:23] [FRONTEND]     },
[2026-03-28 12:50:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:50:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:50:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:50:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:50:23] [FRONTEND]       errno: -61,
[2026-03-28 12:50:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:50:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:50:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:50:23] [FRONTEND]       port: 5001
[2026-03-28 12:50:23] [FRONTEND]     }
[2026-03-28 12:50:23] [FRONTEND]   ]
[2026-03-28 12:50:23] [FRONTEND] }
[2026-03-28 12:51:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:51:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:51:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:51:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:51:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:51:23] [FRONTEND]   [errors]: [
[2026-03-28 12:51:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:51:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:51:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:51:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:51:23] [FRONTEND]       errno: -61,
[2026-03-28 12:51:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:51:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:51:23] [FRONTEND]       address: '::1',
[2026-03-28 12:51:23] [FRONTEND]       port: 5001
[2026-03-28 12:51:23] [FRONTEND]     },
[2026-03-28 12:51:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:51:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:51:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:51:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:51:23] [FRONTEND]       errno: -61,
[2026-03-28 12:51:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:51:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:51:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:51:23] [FRONTEND]       port: 5001
[2026-03-28 12:51:23] [FRONTEND]     }
[2026-03-28 12:51:23] [FRONTEND]   ]
[2026-03-28 12:51:23] [FRONTEND] }
[2026-03-28 12:51:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:51:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:51:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:51:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:51:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:51:23] [FRONTEND]   [errors]: [
[2026-03-28 12:51:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:51:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:51:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:51:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:51:23] [FRONTEND]       errno: -61,
[2026-03-28 12:51:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:51:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:51:23] [FRONTEND]       address: '::1',
[2026-03-28 12:51:23] [FRONTEND]       port: 5001
[2026-03-28 12:51:23] [FRONTEND]     },
[2026-03-28 12:51:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:51:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:51:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:51:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:51:23] [FRONTEND]       errno: -61,
[2026-03-28 12:51:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:51:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:51:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:51:23] [FRONTEND]       port: 5001
[2026-03-28 12:51:23] [FRONTEND]     }
[2026-03-28 12:51:23] [FRONTEND]   ]
[2026-03-28 12:51:23] [FRONTEND] }
[2026-03-28 12:52:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:52:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:52:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:52:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:52:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:52:23] [FRONTEND]   [errors]: [
[2026-03-28 12:52:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:52:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:52:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:52:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:52:23] [FRONTEND]       errno: -61,
[2026-03-28 12:52:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:52:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:52:23] [FRONTEND]       address: '::1',
[2026-03-28 12:52:23] [FRONTEND]       port: 5001
[2026-03-28 12:52:23] [FRONTEND]     },
[2026-03-28 12:52:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:52:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:52:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:52:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:52:23] [FRONTEND]       errno: -61,
[2026-03-28 12:52:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:52:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:52:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:52:23] [FRONTEND]       port: 5001
[2026-03-28 12:52:23] [FRONTEND]     }
[2026-03-28 12:52:23] [FRONTEND]   ]
[2026-03-28 12:52:23] [FRONTEND] }
[2026-03-28 12:52:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:52:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:52:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:52:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:52:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:52:23] [FRONTEND]   [errors]: [
[2026-03-28 12:52:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:52:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:52:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:52:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:52:23] [FRONTEND]       errno: -61,
[2026-03-28 12:52:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:52:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:52:23] [FRONTEND]       address: '::1',
[2026-03-28 12:52:23] [FRONTEND]       port: 5001
[2026-03-28 12:52:23] [FRONTEND]     },
[2026-03-28 12:52:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:52:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:52:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:52:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:52:23] [FRONTEND]       errno: -61,
[2026-03-28 12:52:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:52:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:52:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:52:23] [FRONTEND]       port: 5001
[2026-03-28 12:52:23] [FRONTEND]     }
[2026-03-28 12:52:23] [FRONTEND]   ]
[2026-03-28 12:52:23] [FRONTEND] }
[2026-03-28 12:53:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:53:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:53:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:53:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:53:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:53:23] [FRONTEND]   [errors]: [
[2026-03-28 12:53:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:53:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:53:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:53:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:53:23] [FRONTEND]       errno: -61,
[2026-03-28 12:53:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:53:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:53:23] [FRONTEND]       address: '::1',
[2026-03-28 12:53:23] [FRONTEND]       port: 5001
[2026-03-28 12:53:23] [FRONTEND]     },
[2026-03-28 12:53:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:53:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:53:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:53:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:53:23] [FRONTEND]       errno: -61,
[2026-03-28 12:53:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:53:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:53:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:53:23] [FRONTEND]       port: 5001
[2026-03-28 12:53:23] [FRONTEND]     }
[2026-03-28 12:53:23] [FRONTEND]   ]
[2026-03-28 12:53:23] [FRONTEND] }
[2026-03-28 12:53:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:53:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:53:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:53:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:53:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:53:23] [FRONTEND]   [errors]: [
[2026-03-28 12:53:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:53:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:53:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:53:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:53:23] [FRONTEND]       errno: -61,
[2026-03-28 12:53:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:53:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:53:23] [FRONTEND]       address: '::1',
[2026-03-28 12:53:23] [FRONTEND]       port: 5001
[2026-03-28 12:53:23] [FRONTEND]     },
[2026-03-28 12:53:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:53:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:53:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:53:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:53:23] [FRONTEND]       errno: -61,
[2026-03-28 12:53:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:53:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:53:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:53:23] [FRONTEND]       port: 5001
[2026-03-28 12:53:23] [FRONTEND]     }
[2026-03-28 12:53:23] [FRONTEND]   ]
[2026-03-28 12:53:23] [FRONTEND] }
[2026-03-28 12:54:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:54:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:54:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:54:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:54:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:54:23] [FRONTEND]   [errors]: [
[2026-03-28 12:54:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:54:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:54:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:54:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:54:23] [FRONTEND]       errno: -61,
[2026-03-28 12:54:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:54:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:54:23] [FRONTEND]       address: '::1',
[2026-03-28 12:54:23] [FRONTEND]       port: 5001
[2026-03-28 12:54:23] [FRONTEND]     },
[2026-03-28 12:54:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:54:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:54:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:54:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:54:23] [FRONTEND]       errno: -61,
[2026-03-28 12:54:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:54:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:54:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:54:23] [FRONTEND]       port: 5001
[2026-03-28 12:54:23] [FRONTEND]     }
[2026-03-28 12:54:23] [FRONTEND]   ]
[2026-03-28 12:54:23] [FRONTEND] }
[2026-03-28 12:54:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:54:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:54:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:54:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:54:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:54:23] [FRONTEND]   [errors]: [
[2026-03-28 12:54:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:54:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:54:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:54:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:54:23] [FRONTEND]       errno: -61,
[2026-03-28 12:54:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:54:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:54:23] [FRONTEND]       address: '::1',
[2026-03-28 12:54:23] [FRONTEND]       port: 5001
[2026-03-28 12:54:23] [FRONTEND]     },
[2026-03-28 12:54:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:54:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:54:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:54:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:54:23] [FRONTEND]       errno: -61,
[2026-03-28 12:54:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:54:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:54:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:54:23] [FRONTEND]       port: 5001
[2026-03-28 12:54:23] [FRONTEND]     }
[2026-03-28 12:54:23] [FRONTEND]   ]
[2026-03-28 12:54:23] [FRONTEND] }
[2026-03-28 12:55:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:55:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:55:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:55:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:55:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:55:23] [FRONTEND]   [errors]: [
[2026-03-28 12:55:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:55:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:55:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:55:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:55:23] [FRONTEND]       errno: -61,
[2026-03-28 12:55:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:55:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:55:23] [FRONTEND]       address: '::1',
[2026-03-28 12:55:23] [FRONTEND]       port: 5001
[2026-03-28 12:55:23] [FRONTEND]     },
[2026-03-28 12:55:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:55:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:55:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:55:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:55:23] [FRONTEND]       errno: -61,
[2026-03-28 12:55:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:55:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:55:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:55:23] [FRONTEND]       port: 5001
[2026-03-28 12:55:23] [FRONTEND]     }
[2026-03-28 12:55:23] [FRONTEND]   ]
[2026-03-28 12:55:23] [FRONTEND] }
[2026-03-28 12:55:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:55:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:55:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:55:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:55:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:55:23] [FRONTEND]   [errors]: [
[2026-03-28 12:55:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:55:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:55:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:55:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:55:23] [FRONTEND]       errno: -61,
[2026-03-28 12:55:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:55:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:55:23] [FRONTEND]       address: '::1',
[2026-03-28 12:55:23] [FRONTEND]       port: 5001
[2026-03-28 12:55:23] [FRONTEND]     },
[2026-03-28 12:55:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:55:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:55:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:55:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:55:23] [FRONTEND]       errno: -61,
[2026-03-28 12:55:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:55:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:55:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:55:23] [FRONTEND]       port: 5001
[2026-03-28 12:55:23] [FRONTEND]     }
[2026-03-28 12:55:23] [FRONTEND]   ]
[2026-03-28 12:55:23] [FRONTEND] }
[2026-03-28 12:56:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:56:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:56:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:56:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:56:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:56:23] [FRONTEND]   [errors]: [
[2026-03-28 12:56:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:56:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:56:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:56:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:56:23] [FRONTEND]       errno: -61,
[2026-03-28 12:56:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:56:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:56:23] [FRONTEND]       address: '::1',
[2026-03-28 12:56:23] [FRONTEND]       port: 5001
[2026-03-28 12:56:23] [FRONTEND]     },
[2026-03-28 12:56:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:56:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:56:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:56:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:56:23] [FRONTEND]       errno: -61,
[2026-03-28 12:56:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:56:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:56:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:56:23] [FRONTEND]       port: 5001
[2026-03-28 12:56:23] [FRONTEND]     }
[2026-03-28 12:56:23] [FRONTEND]   ]
[2026-03-28 12:56:23] [FRONTEND] }
[2026-03-28 12:56:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:56:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:56:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:56:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:56:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:56:23] [FRONTEND]   [errors]: [
[2026-03-28 12:56:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:56:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:56:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:56:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:56:23] [FRONTEND]       errno: -61,
[2026-03-28 12:56:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:56:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:56:23] [FRONTEND]       address: '::1',
[2026-03-28 12:56:23] [FRONTEND]       port: 5001
[2026-03-28 12:56:23] [FRONTEND]     },
[2026-03-28 12:56:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:56:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:56:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:56:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:56:23] [FRONTEND]       errno: -61,
[2026-03-28 12:56:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:56:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:56:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:56:23] [FRONTEND]       port: 5001
[2026-03-28 12:56:23] [FRONTEND]     }
[2026-03-28 12:56:23] [FRONTEND]   ]
[2026-03-28 12:56:23] [FRONTEND] }
[2026-03-28 12:57:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:57:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:57:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:57:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:57:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:57:23] [FRONTEND]   [errors]: [
[2026-03-28 12:57:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:57:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:57:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:57:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:57:23] [FRONTEND]       errno: -61,
[2026-03-28 12:57:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:57:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:57:23] [FRONTEND]       address: '::1',
[2026-03-28 12:57:23] [FRONTEND]       port: 5001
[2026-03-28 12:57:23] [FRONTEND]     },
[2026-03-28 12:57:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:57:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:57:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:57:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:57:23] [FRONTEND]       errno: -61,
[2026-03-28 12:57:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:57:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:57:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:57:23] [FRONTEND]       port: 5001
[2026-03-28 12:57:23] [FRONTEND]     }
[2026-03-28 12:57:23] [FRONTEND]   ]
[2026-03-28 12:57:23] [FRONTEND] }
[2026-03-28 12:57:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:57:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:57:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:57:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:57:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:57:23] [FRONTEND]   [errors]: [
[2026-03-28 12:57:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:57:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:57:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:57:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:57:23] [FRONTEND]       errno: -61,
[2026-03-28 12:57:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:57:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:57:23] [FRONTEND]       address: '::1',
[2026-03-28 12:57:23] [FRONTEND]       port: 5001
[2026-03-28 12:57:23] [FRONTEND]     },
[2026-03-28 12:57:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:57:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:57:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:57:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:57:23] [FRONTEND]       errno: -61,
[2026-03-28 12:57:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:57:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:57:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:57:23] [FRONTEND]       port: 5001
[2026-03-28 12:57:23] [FRONTEND]     }
[2026-03-28 12:57:23] [FRONTEND]   ]
[2026-03-28 12:57:23] [FRONTEND] }
[2026-03-28 12:58:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:58:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:58:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:58:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:58:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:58:23] [FRONTEND]   [errors]: [
[2026-03-28 12:58:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:58:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:58:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:58:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:58:23] [FRONTEND]       errno: -61,
[2026-03-28 12:58:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:58:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:58:23] [FRONTEND]       address: '::1',
[2026-03-28 12:58:23] [FRONTEND]       port: 5001
[2026-03-28 12:58:23] [FRONTEND]     },
[2026-03-28 12:58:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:58:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:58:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:58:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:58:23] [FRONTEND]       errno: -61,
[2026-03-28 12:58:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:58:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:58:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:58:23] [FRONTEND]       port: 5001
[2026-03-28 12:58:23] [FRONTEND]     }
[2026-03-28 12:58:23] [FRONTEND]   ]
[2026-03-28 12:58:23] [FRONTEND] }
[2026-03-28 12:58:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:58:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:58:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:58:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:58:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:58:23] [FRONTEND]   [errors]: [
[2026-03-28 12:58:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:58:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:58:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:58:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:58:23] [FRONTEND]       errno: -61,
[2026-03-28 12:58:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:58:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:58:23] [FRONTEND]       address: '::1',
[2026-03-28 12:58:23] [FRONTEND]       port: 5001
[2026-03-28 12:58:23] [FRONTEND]     },
[2026-03-28 12:58:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:58:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:58:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:58:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:58:23] [FRONTEND]       errno: -61,
[2026-03-28 12:58:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:58:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:58:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:58:23] [FRONTEND]       port: 5001
[2026-03-28 12:58:23] [FRONTEND]     }
[2026-03-28 12:58:23] [FRONTEND]   ]
[2026-03-28 12:58:23] [FRONTEND] }
[2026-03-28 12:59:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 12:59:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:59:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:59:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:59:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:59:23] [FRONTEND]   [errors]: [
[2026-03-28 12:59:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:59:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:59:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:59:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:59:23] [FRONTEND]       errno: -61,
[2026-03-28 12:59:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:59:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:59:23] [FRONTEND]       address: '::1',
[2026-03-28 12:59:23] [FRONTEND]       port: 5001
[2026-03-28 12:59:23] [FRONTEND]     },
[2026-03-28 12:59:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:59:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:59:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:59:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:59:23] [FRONTEND]       errno: -61,
[2026-03-28 12:59:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:59:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:59:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:59:23] [FRONTEND]       port: 5001
[2026-03-28 12:59:23] [FRONTEND]     }
[2026-03-28 12:59:23] [FRONTEND]   ]
[2026-03-28 12:59:23] [FRONTEND] }
[2026-03-28 12:59:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 12:59:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 12:59:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 12:59:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:59:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 12:59:23] [FRONTEND]   [errors]: [
[2026-03-28 12:59:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 12:59:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:59:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:59:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:59:23] [FRONTEND]       errno: -61,
[2026-03-28 12:59:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:59:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:59:23] [FRONTEND]       address: '::1',
[2026-03-28 12:59:23] [FRONTEND]       port: 5001
[2026-03-28 12:59:23] [FRONTEND]     },
[2026-03-28 12:59:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 12:59:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 12:59:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 12:59:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 12:59:23] [FRONTEND]       errno: -61,
[2026-03-28 12:59:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 12:59:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 12:59:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 12:59:23] [FRONTEND]       port: 5001
[2026-03-28 12:59:23] [FRONTEND]     }
[2026-03-28 12:59:23] [FRONTEND]   ]
[2026-03-28 12:59:23] [FRONTEND] }
[2026-03-28 13:00:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:00:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:00:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:00:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:00:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:00:23] [FRONTEND]   [errors]: [
[2026-03-28 13:00:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:00:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:00:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:00:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:00:23] [FRONTEND]       errno: -61,
[2026-03-28 13:00:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:00:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:00:23] [FRONTEND]       address: '::1',
[2026-03-28 13:00:23] [FRONTEND]       port: 5001
[2026-03-28 13:00:23] [FRONTEND]     },
[2026-03-28 13:00:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:00:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:00:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:00:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:00:23] [FRONTEND]       errno: -61,
[2026-03-28 13:00:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:00:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:00:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:00:23] [FRONTEND]       port: 5001
[2026-03-28 13:00:23] [FRONTEND]     }
[2026-03-28 13:00:23] [FRONTEND]   ]
[2026-03-28 13:00:23] [FRONTEND] }
[2026-03-28 13:00:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:00:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:00:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:00:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:00:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:00:23] [FRONTEND]   [errors]: [
[2026-03-28 13:00:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:00:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:00:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:00:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:00:23] [FRONTEND]       errno: -61,
[2026-03-28 13:00:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:00:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:00:23] [FRONTEND]       address: '::1',
[2026-03-28 13:00:23] [FRONTEND]       port: 5001
[2026-03-28 13:00:23] [FRONTEND]     },
[2026-03-28 13:00:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:00:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:00:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:00:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:00:23] [FRONTEND]       errno: -61,
[2026-03-28 13:00:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:00:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:00:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:00:23] [FRONTEND]       port: 5001
[2026-03-28 13:00:23] [FRONTEND]     }
[2026-03-28 13:00:23] [FRONTEND]   ]
[2026-03-28 13:00:23] [FRONTEND] }
[2026-03-28 13:01:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:01:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:01:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:01:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:01:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:01:23] [FRONTEND]   [errors]: [
[2026-03-28 13:01:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:01:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:01:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:01:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:01:23] [FRONTEND]       errno: -61,
[2026-03-28 13:01:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:01:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:01:23] [FRONTEND]       address: '::1',
[2026-03-28 13:01:23] [FRONTEND]       port: 5001
[2026-03-28 13:01:23] [FRONTEND]     },
[2026-03-28 13:01:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:01:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:01:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:01:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:01:23] [FRONTEND]       errno: -61,
[2026-03-28 13:01:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:01:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:01:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:01:23] [FRONTEND]       port: 5001
[2026-03-28 13:01:23] [FRONTEND]     }
[2026-03-28 13:01:23] [FRONTEND]   ]
[2026-03-28 13:01:23] [FRONTEND] }
[2026-03-28 13:01:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:01:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:01:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:01:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:01:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:01:23] [FRONTEND]   [errors]: [
[2026-03-28 13:01:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:01:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:01:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:01:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:01:23] [FRONTEND]       errno: -61,
[2026-03-28 13:01:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:01:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:01:23] [FRONTEND]       address: '::1',
[2026-03-28 13:01:23] [FRONTEND]       port: 5001
[2026-03-28 13:01:23] [FRONTEND]     },
[2026-03-28 13:01:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:01:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:01:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:01:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:01:23] [FRONTEND]       errno: -61,
[2026-03-28 13:01:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:01:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:01:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:01:23] [FRONTEND]       port: 5001
[2026-03-28 13:01:23] [FRONTEND]     }
[2026-03-28 13:01:23] [FRONTEND]   ]
[2026-03-28 13:01:23] [FRONTEND] }
[2026-03-28 13:02:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:02:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:02:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:02:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:02:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:02:23] [FRONTEND]   [errors]: [
[2026-03-28 13:02:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:02:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:02:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:02:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:02:23] [FRONTEND]       errno: -61,
[2026-03-28 13:02:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:02:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:02:23] [FRONTEND]       address: '::1',
[2026-03-28 13:02:23] [FRONTEND]       port: 5001
[2026-03-28 13:02:23] [FRONTEND]     },
[2026-03-28 13:02:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:02:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:02:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:02:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:02:23] [FRONTEND]       errno: -61,
[2026-03-28 13:02:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:02:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:02:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:02:23] [FRONTEND]       port: 5001
[2026-03-28 13:02:23] [FRONTEND]     }
[2026-03-28 13:02:23] [FRONTEND]   ]
[2026-03-28 13:02:23] [FRONTEND] }
[2026-03-28 13:02:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:02:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:02:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:02:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:02:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:02:23] [FRONTEND]   [errors]: [
[2026-03-28 13:02:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:02:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:02:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:02:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:02:23] [FRONTEND]       errno: -61,
[2026-03-28 13:02:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:02:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:02:23] [FRONTEND]       address: '::1',
[2026-03-28 13:02:23] [FRONTEND]       port: 5001
[2026-03-28 13:02:23] [FRONTEND]     },
[2026-03-28 13:02:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:02:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:02:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:02:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:02:23] [FRONTEND]       errno: -61,
[2026-03-28 13:02:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:02:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:02:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:02:23] [FRONTEND]       port: 5001
[2026-03-28 13:02:23] [FRONTEND]     }
[2026-03-28 13:02:23] [FRONTEND]   ]
[2026-03-28 13:02:23] [FRONTEND] }
[2026-03-28 13:03:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:03:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:03:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:03:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:03:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:03:23] [FRONTEND]   [errors]: [
[2026-03-28 13:03:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:03:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:03:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:03:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:03:23] [FRONTEND]       errno: -61,
[2026-03-28 13:03:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:03:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:03:23] [FRONTEND]       address: '::1',
[2026-03-28 13:03:23] [FRONTEND]       port: 5001
[2026-03-28 13:03:23] [FRONTEND]     },
[2026-03-28 13:03:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:03:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:03:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:03:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:03:23] [FRONTEND]       errno: -61,
[2026-03-28 13:03:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:03:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:03:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:03:23] [FRONTEND]       port: 5001
[2026-03-28 13:03:23] [FRONTEND]     }
[2026-03-28 13:03:23] [FRONTEND]   ]
[2026-03-28 13:03:23] [FRONTEND] }
[2026-03-28 13:03:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:03:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:03:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:03:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:03:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:03:23] [FRONTEND]   [errors]: [
[2026-03-28 13:03:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:03:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:03:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:03:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:03:23] [FRONTEND]       errno: -61,
[2026-03-28 13:03:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:03:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:03:23] [FRONTEND]       address: '::1',
[2026-03-28 13:03:23] [FRONTEND]       port: 5001
[2026-03-28 13:03:23] [FRONTEND]     },
[2026-03-28 13:03:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:03:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:03:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:03:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:03:23] [FRONTEND]       errno: -61,
[2026-03-28 13:03:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:03:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:03:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:03:23] [FRONTEND]       port: 5001
[2026-03-28 13:03:23] [FRONTEND]     }
[2026-03-28 13:03:23] [FRONTEND]   ]
[2026-03-28 13:03:23] [FRONTEND] }
[2026-03-28 13:04:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:04:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:04:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:04:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:04:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:04:23] [FRONTEND]   [errors]: [
[2026-03-28 13:04:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:04:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:04:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:04:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:04:23] [FRONTEND]       errno: -61,
[2026-03-28 13:04:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:04:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:04:23] [FRONTEND]       address: '::1',
[2026-03-28 13:04:23] [FRONTEND]       port: 5001
[2026-03-28 13:04:23] [FRONTEND]     },
[2026-03-28 13:04:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:04:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:04:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:04:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:04:23] [FRONTEND]       errno: -61,
[2026-03-28 13:04:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:04:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:04:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:04:23] [FRONTEND]       port: 5001
[2026-03-28 13:04:23] [FRONTEND]     }
[2026-03-28 13:04:23] [FRONTEND]   ]
[2026-03-28 13:04:23] [FRONTEND] }
[2026-03-28 13:04:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:04:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:04:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:04:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:04:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:04:23] [FRONTEND]   [errors]: [
[2026-03-28 13:04:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:04:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:04:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:04:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:04:23] [FRONTEND]       errno: -61,
[2026-03-28 13:04:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:04:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:04:23] [FRONTEND]       address: '::1',
[2026-03-28 13:04:23] [FRONTEND]       port: 5001
[2026-03-28 13:04:23] [FRONTEND]     },
[2026-03-28 13:04:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:04:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:04:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:04:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:04:23] [FRONTEND]       errno: -61,
[2026-03-28 13:04:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:04:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:04:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:04:23] [FRONTEND]       port: 5001
[2026-03-28 13:04:23] [FRONTEND]     }
[2026-03-28 13:04:23] [FRONTEND]   ]
[2026-03-28 13:04:23] [FRONTEND] }
[2026-03-28 13:05:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:05:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:05:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:05:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:05:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:05:23] [FRONTEND]   [errors]: [
[2026-03-28 13:05:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:05:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:05:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:05:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:05:23] [FRONTEND]       errno: -61,
[2026-03-28 13:05:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:05:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:05:23] [FRONTEND]       address: '::1',
[2026-03-28 13:05:23] [FRONTEND]       port: 5001
[2026-03-28 13:05:23] [FRONTEND]     },
[2026-03-28 13:05:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:05:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:05:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:05:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:05:23] [FRONTEND]       errno: -61,
[2026-03-28 13:05:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:05:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:05:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:05:23] [FRONTEND]       port: 5001
[2026-03-28 13:05:23] [FRONTEND]     }
[2026-03-28 13:05:23] [FRONTEND]   ]
[2026-03-28 13:05:23] [FRONTEND] }
[2026-03-28 13:05:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:05:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:05:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:05:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:05:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:05:23] [FRONTEND]   [errors]: [
[2026-03-28 13:05:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:05:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:05:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:05:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:05:23] [FRONTEND]       errno: -61,
[2026-03-28 13:05:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:05:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:05:23] [FRONTEND]       address: '::1',
[2026-03-28 13:05:23] [FRONTEND]       port: 5001
[2026-03-28 13:05:23] [FRONTEND]     },
[2026-03-28 13:05:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:05:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:05:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:05:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:05:23] [FRONTEND]       errno: -61,
[2026-03-28 13:05:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:05:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:05:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:05:23] [FRONTEND]       port: 5001
[2026-03-28 13:05:23] [FRONTEND]     }
[2026-03-28 13:05:23] [FRONTEND]   ]
[2026-03-28 13:05:23] [FRONTEND] }
[2026-03-28 13:06:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:06:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:06:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:06:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:06:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:06:23] [FRONTEND]   [errors]: [
[2026-03-28 13:06:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:06:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:06:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:06:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:06:23] [FRONTEND]       errno: -61,
[2026-03-28 13:06:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:06:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:06:23] [FRONTEND]       address: '::1',
[2026-03-28 13:06:23] [FRONTEND]       port: 5001
[2026-03-28 13:06:23] [FRONTEND]     },
[2026-03-28 13:06:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:06:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:06:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:06:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:06:23] [FRONTEND]       errno: -61,
[2026-03-28 13:06:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:06:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:06:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:06:23] [FRONTEND]       port: 5001
[2026-03-28 13:06:23] [FRONTEND]     }
[2026-03-28 13:06:23] [FRONTEND]   ]
[2026-03-28 13:06:23] [FRONTEND] }
[2026-03-28 13:06:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:06:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:06:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:06:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:06:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:06:23] [FRONTEND]   [errors]: [
[2026-03-28 13:06:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:06:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:06:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:06:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:06:23] [FRONTEND]       errno: -61,
[2026-03-28 13:06:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:06:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:06:23] [FRONTEND]       address: '::1',
[2026-03-28 13:06:23] [FRONTEND]       port: 5001
[2026-03-28 13:06:23] [FRONTEND]     },
[2026-03-28 13:06:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:06:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:06:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:06:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:06:23] [FRONTEND]       errno: -61,
[2026-03-28 13:06:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:06:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:06:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:06:23] [FRONTEND]       port: 5001
[2026-03-28 13:06:23] [FRONTEND]     }
[2026-03-28 13:06:23] [FRONTEND]   ]
[2026-03-28 13:06:23] [FRONTEND] }
[2026-03-28 13:07:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:07:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:07:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:07:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:07:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:07:23] [FRONTEND]   [errors]: [
[2026-03-28 13:07:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:07:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:07:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:07:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:07:23] [FRONTEND]       errno: -61,
[2026-03-28 13:07:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:07:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:07:23] [FRONTEND]       address: '::1',
[2026-03-28 13:07:23] [FRONTEND]       port: 5001
[2026-03-28 13:07:23] [FRONTEND]     },
[2026-03-28 13:07:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:07:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:07:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:07:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:07:23] [FRONTEND]       errno: -61,
[2026-03-28 13:07:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:07:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:07:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:07:23] [FRONTEND]       port: 5001
[2026-03-28 13:07:23] [FRONTEND]     }
[2026-03-28 13:07:23] [FRONTEND]   ]
[2026-03-28 13:07:23] [FRONTEND] }
[2026-03-28 13:07:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:07:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:07:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:07:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:07:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:07:23] [FRONTEND]   [errors]: [
[2026-03-28 13:07:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:07:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:07:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:07:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:07:23] [FRONTEND]       errno: -61,
[2026-03-28 13:07:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:07:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:07:23] [FRONTEND]       address: '::1',
[2026-03-28 13:07:23] [FRONTEND]       port: 5001
[2026-03-28 13:07:23] [FRONTEND]     },
[2026-03-28 13:07:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:07:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:07:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:07:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:07:23] [FRONTEND]       errno: -61,
[2026-03-28 13:07:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:07:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:07:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:07:23] [FRONTEND]       port: 5001
[2026-03-28 13:07:23] [FRONTEND]     }
[2026-03-28 13:07:23] [FRONTEND]   ]
[2026-03-28 13:07:23] [FRONTEND] }
[2026-03-28 13:08:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:08:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:08:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:08:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:08:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:08:23] [FRONTEND]   [errors]: [
[2026-03-28 13:08:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:08:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:08:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:08:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:08:23] [FRONTEND]       errno: -61,
[2026-03-28 13:08:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:08:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:08:23] [FRONTEND]       address: '::1',
[2026-03-28 13:08:23] [FRONTEND]       port: 5001
[2026-03-28 13:08:23] [FRONTEND]     },
[2026-03-28 13:08:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:08:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:08:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:08:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:08:23] [FRONTEND]       errno: -61,
[2026-03-28 13:08:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:08:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:08:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:08:23] [FRONTEND]       port: 5001
[2026-03-28 13:08:23] [FRONTEND]     }
[2026-03-28 13:08:23] [FRONTEND]   ]
[2026-03-28 13:08:23] [FRONTEND] }
[2026-03-28 13:08:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:08:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:08:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:08:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:08:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:08:23] [FRONTEND]   [errors]: [
[2026-03-28 13:08:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:08:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:08:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:08:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:08:23] [FRONTEND]       errno: -61,
[2026-03-28 13:08:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:08:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:08:23] [FRONTEND]       address: '::1',
[2026-03-28 13:08:23] [FRONTEND]       port: 5001
[2026-03-28 13:08:23] [FRONTEND]     },
[2026-03-28 13:08:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:08:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:08:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:08:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:08:23] [FRONTEND]       errno: -61,
[2026-03-28 13:08:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:08:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:08:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:08:23] [FRONTEND]       port: 5001
[2026-03-28 13:08:23] [FRONTEND]     }
[2026-03-28 13:08:23] [FRONTEND]   ]
[2026-03-28 13:08:23] [FRONTEND] }
[2026-03-28 13:09:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:09:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:09:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:09:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:09:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:09:23] [FRONTEND]   [errors]: [
[2026-03-28 13:09:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:09:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:09:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:09:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:09:23] [FRONTEND]       errno: -61,
[2026-03-28 13:09:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:09:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:09:23] [FRONTEND]       address: '::1',
[2026-03-28 13:09:23] [FRONTEND]       port: 5001
[2026-03-28 13:09:23] [FRONTEND]     },
[2026-03-28 13:09:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:09:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:09:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:09:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:09:23] [FRONTEND]       errno: -61,
[2026-03-28 13:09:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:09:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:09:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:09:23] [FRONTEND]       port: 5001
[2026-03-28 13:09:23] [FRONTEND]     }
[2026-03-28 13:09:23] [FRONTEND]   ]
[2026-03-28 13:09:23] [FRONTEND] }
[2026-03-28 13:09:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:09:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:09:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:09:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:09:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:09:23] [FRONTEND]   [errors]: [
[2026-03-28 13:09:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:09:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:09:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:09:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:09:23] [FRONTEND]       errno: -61,
[2026-03-28 13:09:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:09:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:09:23] [FRONTEND]       address: '::1',
[2026-03-28 13:09:23] [FRONTEND]       port: 5001
[2026-03-28 13:09:23] [FRONTEND]     },
[2026-03-28 13:09:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:09:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:09:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:09:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:09:23] [FRONTEND]       errno: -61,
[2026-03-28 13:09:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:09:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:09:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:09:23] [FRONTEND]       port: 5001
[2026-03-28 13:09:23] [FRONTEND]     }
[2026-03-28 13:09:23] [FRONTEND]   ]
[2026-03-28 13:09:23] [FRONTEND] }
[2026-03-28 13:10:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:10:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:10:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:10:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:10:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:10:23] [FRONTEND]   [errors]: [
[2026-03-28 13:10:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:10:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:10:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:10:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:10:23] [FRONTEND]       errno: -61,
[2026-03-28 13:10:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:10:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:10:23] [FRONTEND]       address: '::1',
[2026-03-28 13:10:23] [FRONTEND]       port: 5001
[2026-03-28 13:10:23] [FRONTEND]     },
[2026-03-28 13:10:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:10:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:10:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:10:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:10:23] [FRONTEND]       errno: -61,
[2026-03-28 13:10:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:10:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:10:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:10:23] [FRONTEND]       port: 5001
[2026-03-28 13:10:23] [FRONTEND]     }
[2026-03-28 13:10:23] [FRONTEND]   ]
[2026-03-28 13:10:23] [FRONTEND] }
[2026-03-28 13:10:23] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:10:23] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:10:23] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:10:23] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:10:23] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:10:23] [FRONTEND]   [errors]: [
[2026-03-28 13:10:23] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:10:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:10:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:10:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:10:23] [FRONTEND]       errno: -61,
[2026-03-28 13:10:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:10:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:10:23] [FRONTEND]       address: '::1',
[2026-03-28 13:10:23] [FRONTEND]       port: 5001
[2026-03-28 13:10:23] [FRONTEND]     },
[2026-03-28 13:10:23] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:10:23] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:10:23] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:10:23] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:10:23] [FRONTEND]       errno: -61,
[2026-03-28 13:10:23] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:10:23] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:10:23] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:10:23] [FRONTEND]       port: 5001
[2026-03-28 13:10:23] [FRONTEND]     }
[2026-03-28 13:10:23] [FRONTEND]   ]
[2026-03-28 13:10:23] [FRONTEND] }
[2026-03-28 13:11:24] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 13:11:24] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:11:24] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:11:24] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:11:24] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:11:24] [FRONTEND]   [errors]: [
[2026-03-28 13:11:24] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:11:24] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:11:24] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:11:24] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:11:24] [FRONTEND]       errno: -61,
[2026-03-28 13:11:24] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:11:24] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:11:24] [FRONTEND]       address: '::1',
[2026-03-28 13:11:24] [FRONTEND]       port: 5001
[2026-03-28 13:11:24] [FRONTEND]     },
[2026-03-28 13:11:24] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:11:24] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:11:24] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:11:24] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:11:24] [FRONTEND]       errno: -61,
[2026-03-28 13:11:24] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:11:24] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:11:24] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:11:24] [FRONTEND]       port: 5001
[2026-03-28 13:11:24] [FRONTEND]     }
[2026-03-28 13:11:24] [FRONTEND]   ]
[2026-03-28 13:11:24] [FRONTEND] }
[2026-03-28 13:11:24] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 13:11:24] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 13:11:24] [FRONTEND]     at afterConnectMultiple (node:net:1689:7)
[2026-03-28 13:11:24] [FRONTEND]     at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:11:24] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 13:11:24] [FRONTEND]   [errors]: [
[2026-03-28 13:11:24] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 13:11:24] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:11:24] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:11:24] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:11:24] [FRONTEND]       errno: -61,
[2026-03-28 13:11:24] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:11:24] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:11:24] [FRONTEND]       address: '::1',
[2026-03-28 13:11:24] [FRONTEND]       port: 5001
[2026-03-28 13:11:24] [FRONTEND]     },
[2026-03-28 13:11:24] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 13:11:24] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 13:11:24] [FRONTEND]         at afterConnectMultiple (node:net:1682:16)
[2026-03-28 13:11:24] [FRONTEND]         at TCPConnectWrap.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:11:24] [FRONTEND]       errno: -61,
[2026-03-28 13:11:24] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 13:11:24] [FRONTEND]       syscall: 'connect',
[2026-03-28 13:11:24] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 13:11:24] [FRONTEND]       port: 5001
[2026-03-28 13:11:24] [FRONTEND]     }
[2026-03-28 13:11:24] [FRONTEND]   ]
[2026-03-28 13:11:24] [FRONTEND] }


---
**YENİ OTURUM BAŞLADI:** Sat Mar 28 13:11:28 +03 2026
---

[2026-03-28 13:11:29] [BACKEND] >>> Sicilius Backend Startup Sequence Initiated <<<
[2026-03-28 13:11:29] [BACKEND] [+] Eski (zombi) SSH tüneli bulundu, temizleniyor...
[2026-03-28 13:11:29] [FRONTEND] yarn run v1.22.22
[2026-03-28 13:11:29] [FRONTEND] $ next dev
[2026-03-28 13:11:30] [FRONTEND]   ▲ Next.js 14.2.3
[2026-03-28 13:11:30] [FRONTEND]   - Local:        http://localhost:3000
[2026-03-28 13:11:30] [FRONTEND]   - Environments: .env.local
[2026-03-28 13:11:30] [FRONTEND] 
[2026-03-28 13:11:30] [FRONTEND]  ✓ Starting...
[2026-03-28 13:11:30] [DOCLING] 2026-03-28 13:11:30,780 - INFO - No GPU detected, using CPU.
[2026-03-28 13:11:30] [DOCLING] 2026-03-28 13:11:30,780 - INFO - Starting Docling Fast Server on http://0.0.0.0:5002
[2026-03-28 13:11:30] [DOCLING] 2026-03-28 13:11:30,780 - INFO - OCR settings: force_ocr=False, lang=default
[2026-03-28 13:11:30] [DOCLING] INFO:     Started server process [13174]
[2026-03-28 13:11:30] [DOCLING] INFO:     Waiting for application startup.
[2026-03-28 13:11:30] [DOCLING] 2026-03-28 13:11:30,812 - INFO - Initializing DocumentConverter (force_ocr=False, lang=default, enrichments=none)...
[2026-03-28 13:11:31] [BACKEND] [+] Yeni SSH database tüneli kuruluyor. Uzak veritabanı IP'si bulunuyor...
[2026-03-28 13:11:32] [FRONTEND]  ✓ Ready in 1965ms
[2026-03-28 13:11:33] [BACKEND] [+] Remote database IP found: 172.18.0.6. Establishing tunnel...
[2026-03-28 13:11:33] [BACKEND] [+] SSH Tunnel successfully established to 172.18.0.6.
[2026-03-28 13:11:33] [BACKEND] [+] Starting FastAPI server...
[2026-03-28 13:11:36] [DOCLING] 2026-03-28 13:11:36,613 - INFO - DocumentConverter initialized in 5.80s
[2026-03-28 13:11:36] [DOCLING] INFO:     Application startup complete.
[2026-03-28 13:11:36] [DOCLING] ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 5002): address already in use
[2026-03-28 13:11:36] [DOCLING] INFO:     Waiting for application shutdown.
[2026-03-28 13:11:36] [DOCLING] INFO:     Application shutdown complete.
[2026-03-28 13:11:37] [DOCLING] cd backend && opendataloader-pdf-hybrid --port 5002 exited with code 1
[2026-03-28 13:11:37] [CELERY]  
[2026-03-28 13:11:37] [CELERY]  -------------- celery@192.168.1.8 v5.3.4 (emerald-rush)
[2026-03-28 13:11:37] [CELERY] --- ***** ----- 
[2026-03-28 13:11:37] [CELERY] -- ******* ---- macOS-26.3.1-arm64-arm-64bit 2026-03-28 13:11:37
[2026-03-28 13:11:37] [CELERY] - *** --- * --- 
[2026-03-28 13:11:37] [CELERY] - ** ---------- [config]
[2026-03-28 13:11:37] [CELERY] - ** ---------- .> app:         worker:0x1078d6170
[2026-03-28 13:11:37] [CELERY] - ** ---------- .> transport:   redis://localhost:6379/0
[2026-03-28 13:11:37] [CELERY] - ** ---------- .> results:     redis://localhost:6379/0
[2026-03-28 13:11:37] [CELERY] - *** --- * --- .> concurrency: 8 (solo)
[2026-03-28 13:11:37] [CELERY] -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
[2026-03-28 13:11:37] [CELERY] --- ***** ----- 
[2026-03-28 13:11:37] [CELERY]  -------------- [queues]
[2026-03-28 13:11:37] [CELERY]                 .> celery           exchange=celery(direct) key=celery
[2026-03-28 13:11:37] [CELERY]                 
[2026-03-28 13:11:37] [CELERY] 
[2026-03-28 13:11:37] [CELERY] [tasks]
[2026-03-28 13:11:37] [CELERY]   . app.tasks.ocr_tasks.run_historical_ocr_backfill
[2026-03-28 13:11:37] [CELERY]   . app.tasks.scraping_tasks.run_scraping_task
[2026-03-28 13:11:37] [CELERY] 
[2026-03-28 13:11:37] [CELERY] 2026-03-28 13:11:37,524 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 13:11:37] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 13:11:37] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 13:11:37] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 13:11:37] [CELERY]   warnings.warn(
[2026-03-28 13:11:37] [CELERY] 
[2026-03-28 13:11:37] [CELERY] 2026-03-28 13:11:37,528 - celery.worker.consumer.connection - INFO - Connected to redis://localhost:6379/0
[2026-03-28 13:11:37] [CELERY] 2026-03-28 13:11:37,528 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 13:11:37] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 13:11:37] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 13:11:37] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 13:11:37] [CELERY]   warnings.warn(
[2026-03-28 13:11:37] [CELERY] 
[2026-03-28 13:11:37] [CELERY] 2026-03-28 13:11:37,530 - celery.worker.consumer.mingle - INFO - mingle: searching for neighbors
[2026-03-28 13:11:38] [CELERY] 2026-03-28 13:11:38,537 - celery.worker.consumer.mingle - INFO - mingle: all alone
[2026-03-28 13:11:38] [CELERY] 2026-03-28 13:11:38,543 - celery.apps.worker - INFO - celery@192.168.1.8 ready.
[2026-03-28 13:11:41] [BACKEND] INFO:     Started server process [13226]
[2026-03-28 13:11:41] [BACKEND] INFO:     Waiting for application startup.
[2026-03-28 13:11:42] [BACKEND] INFO:     Application startup complete.
[2026-03-28 13:11:42] [BACKEND] INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
[2026-03-28 13:11:46] [FRONTEND]  ✓ Compiled /api/v1/search/company-detail in 387ms (53 modules)
[2026-03-28 13:11:48] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 200 in 1746ms
[2026-03-28 13:11:48] [FRONTEND]  ✓ Compiled /src/middleware in 74ms (73 modules)
[2026-03-28 13:11:49] [FRONTEND]  ○ Compiling /dashboard ...
[2026-03-28 13:11:51] [FRONTEND]  ✓ Compiled /dashboard in 2.2s (4552 modules)
[2026-03-28 13:11:51] [FRONTEND]  GET /dashboard/ 200 in 2456ms
[2026-03-28 13:11:51] [FRONTEND]  ○ Compiling /manifest.webmanifest ...
[2026-03-28 13:11:52] [BACKEND] 2026-03-28 13:11:52,123 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-28 13:11:52] [FRONTEND]  ✓ Compiled /manifest.webmanifest in 843ms (4585 modules)
[2026-03-28 13:11:52] [BACKEND] 2026-03-28 13:11:52,242 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-28 13:11:52] [FRONTEND]  GET /.well-known/appspecific/com.chrome.devtools.json 404 in 1091ms
[2026-03-28 13:11:52] [FRONTEND]  GET /manifest.webmanifest 200 in 1103ms
[2026-03-28 13:11:52] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:11:52] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:12:10] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:12:12] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=340b3ab7-8b32-4d1a-ac90-bcfaeba4470f 200 in 790ms
[2026-03-28 13:12:12] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:12:53] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:13:52] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:14:00] [BACKEND] 2026-03-28 13:14:00,872 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company 9c04ca14-ee38-45e9-9024-48311570bb9c: 'İvedikosb Mah. 1370 Cad. No: 15 Yenimahalle / Ankara'
[2026-03-28 13:14:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:14:26] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=30a24cfb-a97c-4c7a-b386-cd7bbcbb4b5b 200 in 491ms
[2026-03-28 13:14:26] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:14:52] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:15:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:15:21] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=fdc6e32b-2324-4726-9bd2-e003f1dcff87 200 in 488ms
[2026-03-28 13:15:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:15:28] [BACKEND] 2026-03-28 13:15:28,226 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company 9c04ca14-ee38-45e9-9024-48311570bb9c: 'İvedikosb Mah. 1370 Cad. No: 15 Yenimahalle / Ankara'
[2026-03-28 13:15:52] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:17:23] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me Error: socket hang up
[2026-03-28 13:17:23] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 13:17:23] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 13:17:23] [FRONTEND]     at TCP.<anonymous> (node:net:343:12)
[2026-03-28 13:17:23] [FRONTEND]     at TCP.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:17:23] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 13:17:23] [FRONTEND] }
[2026-03-28 13:17:23] [FRONTEND] Error: socket hang up
[2026-03-28 13:17:23] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 13:17:23] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 13:17:23] [FRONTEND]     at TCP.<anonymous> (node:net:343:12)
[2026-03-28 13:17:23] [FRONTEND]     at TCP.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:17:23] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 13:17:23] [FRONTEND] }
[2026-03-28 13:17:23] [FRONTEND]  ○ Compiling /_error ...
[2026-03-28 13:17:23] [FRONTEND]  ✓ Compiled /_error in 668ms (4782 modules)
[2026-03-28 13:17:29] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:17:30] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=fdc6e32b-2324-4726-9bd2-e003f1dcff87 200 in 20535ms
[2026-03-28 13:17:30] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:17:46] [BACKEND] 2026-03-28 13:17:46,790 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company 9c04ca14-ee38-45e9-9024-48311570bb9c: 'İvedikosb Mah. 1370 Cad. No: 15 Yenimahalle / Ankara'
[2026-03-28 13:17:53] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:18:19] [BACKEND] 2026-03-28 13:18:19,507 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company 9c04ca14-ee38-45e9-9024-48311570bb9c: 'İvedikosb Mah. 1370 Cad. No: 15 Yenimahalle / Ankara'
[2026-03-28 13:18:55] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:19:49] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/search/all?q=gemsan%20grup&cursor=0&limit=20 Error: socket hang up
[2026-03-28 13:19:49] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 13:19:49] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 13:19:49] [FRONTEND]     at TCP.<anonymous> (node:net:343:12)
[2026-03-28 13:19:49] [FRONTEND]     at TCP.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:19:49] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 13:19:49] [FRONTEND] }
[2026-03-28 13:19:49] [FRONTEND] Error: socket hang up
[2026-03-28 13:19:49] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 13:19:49] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 13:19:49] [FRONTEND]     at TCP.<anonymous> (node:net:343:12)
[2026-03-28 13:19:49] [FRONTEND]     at TCP.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 13:19:49] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 13:19:49] [FRONTEND] }
[2026-03-28 13:19:52] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:20:53] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:21:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:21:03] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=fdc6e32b-2324-4726-9bd2-e003f1dcff87 200 in 730ms
[2026-03-28 13:21:03] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:21:04] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:21:32] [BACKEND] 2026-03-28 13:21:32,258 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company 9c04ca14-ee38-45e9-9024-48311570bb9c: 'İvedikosb Mah. 1370 Cad. No: 15 Yenimahalle / Ankara'
[2026-03-28 13:21:42] [BACKEND] 2026-03-28 13:21:42,624 - app.api.api_v1.endpoints.processing - WARNING - Could not geocode address via engine for company 9c04ca14-ee38-45e9-9024-48311570bb9c: 'İvedikosb Mah. 1370 Cad. No: 15 Yenimahalle / Ankara'
[2026-03-28 13:21:52] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:22:09] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:22:11] [FRONTEND]  GET /api/v1/search/company-detail/?company_id=37bca066-c162-4eb2-9800-a8dfb21f105a 200 in 531ms
[2026-03-28 13:22:11] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:22:53] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:24:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:25:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:26:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:27:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:28:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:29:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:30:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:31:35] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:32:26] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:33:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:34:32] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:35:33] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:36:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:37:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:38:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:39:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:40:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:41:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:42:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:43:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:44:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:45:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:46:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:47:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:48:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:49:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:49:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:50:53] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:52:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:53:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:54:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:55:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:56:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:57:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:58:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 13:59:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:00:24] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:01:27] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:13:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:14:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:15:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:16:11] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:17:10] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:18:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:19:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:20:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:21:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:22:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:23:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:26:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:27:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:28:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:29:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:30:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:31:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:32:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:33:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:34:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:35:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:36:20] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:37:48] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:41:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:48:37] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:49:37] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:50:36] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:51:37] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:52:36] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:53:36] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:54:36] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:55:36] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:56:36] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:57:36] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:58:36] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 14:59:37] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:00:37] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:06:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:08:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:08:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:09:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:10:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:12:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:12:17] [FRONTEND]  ○ Compiling /admin/ocr-management ...
[2026-03-28 15:12:18] [FRONTEND]  ✓ Compiled /admin/ocr-management in 1712ms (7991 modules)
[2026-03-28 15:12:18] [FRONTEND]  ✓ Compiled /manifest.webmanifest in 180ms (3997 modules)
[2026-03-28 15:12:18] [FRONTEND]  GET /manifest.webmanifest 200 in 224ms
[2026-03-28 15:12:19] [BACKEND] 2026-03-28 15:12:19,069 - app.api.api_v1.endpoints.users - WARNING - [/users/me] user=turgaykirkil@me.com role=admin
[2026-03-28 15:12:19] [BACKEND] DEBUG: require-admin entered for turgaykirkil@me.com
[2026-03-28 15:12:19] [BACKEND] DEBUG: require-admin check: is_admin=True
[2026-03-28 15:12:19] [BACKEND] 2026-03-28 15:12:19,126 - app.api.api_v1.endpoints.auth - WARNING - [require-admin] user=turgaykirkil@me.com role=admin is_admin=True
[2026-03-28 15:12:20] [BACKEND] DEBUG: require-admin entered for turgaykirkil@me.com
[2026-03-28 15:12:20] [BACKEND] DEBUG: require-admin check: is_admin=True
[2026-03-28 15:12:20] [BACKEND] 2026-03-28 15:12:20,911 - app.api.api_v1.endpoints.auth - WARNING - [require-admin] user=turgaykirkil@me.com role=admin is_admin=True
[2026-03-28 15:12:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:13:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:15:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:16:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:16:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:18:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:18:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:20:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:20:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:22:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:23:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:24:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:25:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:26:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:27:07] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:27:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:29:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:29:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:30:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:32:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:33:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:34:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:35:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:36:04] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:37:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:38:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:39:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:40:29] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me Error: socket hang up
[2026-03-28 15:40:29] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 15:40:29] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 15:40:29] [FRONTEND]     at TCP.<anonymous> (node:net:343:12)
[2026-03-28 15:40:29] [FRONTEND]     at TCP.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 15:40:29] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 15:40:29] [FRONTEND] }
[2026-03-28 15:40:29] [FRONTEND] Error: socket hang up
[2026-03-28 15:40:29] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 15:40:29] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 15:40:29] [FRONTEND]     at TCP.<anonymous> (node:net:343:12)
[2026-03-28 15:40:29] [FRONTEND]     at TCP.callbackTrampoline (node:internal/async_hooks:130:17) {
[2026-03-28 15:40:29] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 15:40:29] [FRONTEND] }
[2026-03-28 15:40:30] [FRONTEND]  ○ Compiling /_error ...
[2026-03-28 15:40:30] [FRONTEND]  ✓ Compiled /_error in 653ms (6371 modules)
[2026-03-28 15:40:37] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:41:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:42:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:43:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:44:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:45:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:46:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:46:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:47:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:49:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:49:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:50:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:52:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:52:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:54:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:55:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:55:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:57:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:58:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:59:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 15:59:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:01:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:02:08] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:02:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:04:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:05:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:06:08] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:06:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:07:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:09:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:09:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:11:07] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:11:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:13:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:13:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:14:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:16:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:17:23] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:18:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:19:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:20:03] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:21:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:22:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:23:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:23:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:25:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:26:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:27:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:28:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:29:08] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:29:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:31:13] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:32:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:33:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:34:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:34:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:36:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:37:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:38:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:38:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:40:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:41:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:42:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:43:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:44:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:45:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:46:17] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:47:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:48:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:49:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:50:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:50:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:52:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:53:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:54:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:55:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:56:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:57:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:58:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 16:58:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:00:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:00:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:01:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:03:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:03:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:04:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:05:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:07:09] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:08:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:08:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:10:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:11:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:12:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:13:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:14:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:15:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:15:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:17:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:17:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa


---
**YENİ OTURUM BAŞLADI:** Sat Mar 28 17:19:53 +03 2026
---

[2026-03-28 17:19:54] [FRONTEND] yarn run v1.22.22
[2026-03-28 17:19:54] [FRONTEND] $ next dev
[2026-03-28 17:19:54] [BACKEND] >>> Sicilius Backend Startup Sequence Initiated <<<
[2026-03-28 17:19:55] [BACKEND] [+] Eski (zombi) SSH tüneli bulundu, temizleniyor...
[2026-03-28 17:19:55] [FRONTEND]   ▲ Next.js 14.2.3
[2026-03-28 17:19:55] [FRONTEND]   - Local:        http://localhost:3000
[2026-03-28 17:19:55] [FRONTEND]   - Environments: .env.local
[2026-03-28 17:19:55] [FRONTEND] 
[2026-03-28 17:19:55] [FRONTEND]  ✓ Starting...
[2026-03-28 17:19:56] [DOCLING] 2026-03-28 17:19:56,168 - INFO - No GPU detected, using CPU.
[2026-03-28 17:19:56] [DOCLING] 2026-03-28 17:19:56,168 - INFO - Starting Docling Fast Server on http://0.0.0.0:5002
[2026-03-28 17:19:56] [DOCLING] 2026-03-28 17:19:56,168 - INFO - OCR settings: force_ocr=False, lang=default
[2026-03-28 17:19:56] [DOCLING] INFO:     Started server process [93297]
[2026-03-28 17:19:56] [DOCLING] INFO:     Waiting for application startup.
[2026-03-28 17:19:56] [DOCLING] 2026-03-28 17:19:56,197 - INFO - Initializing DocumentConverter (force_ocr=False, lang=default, enrichments=none)...
[2026-03-28 17:19:56] [BACKEND] [+] Yeni SSH database tüneli kuruluyor. Uzak veritabanı IP'si bulunuyor...
[2026-03-28 17:19:57] [FRONTEND]  ✓ Ready in 2.2s
[2026-03-28 17:19:58] [BACKEND] [+] Remote database IP found: 172.18.0.6. Establishing tunnel...
[2026-03-28 17:19:59] [BACKEND] bind [127.0.0.1]:9000: Address already in use
[2026-03-28 17:19:59] [BACKEND] channel_setup_fwd_listener_tcpip: cannot listen to port: 9000
[2026-03-28 17:19:59] [BACKEND] [+] SSH Tunnel successfully established to 172.18.0.6.
[2026-03-28 17:19:59] [BACKEND] [+] Starting FastAPI server...
[2026-03-28 17:19:59] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/ocr/stats AggregateError [ECONNREFUSED]: 
[2026-03-28 17:19:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 17:19:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 17:19:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]   [errors]: [
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '::1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     },
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     }
[2026-03-28 17:19:59] [FRONTEND]   ]
[2026-03-28 17:19:59] [FRONTEND] }
[2026-03-28 17:19:59] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 17:19:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 17:19:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 17:19:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]   [errors]: [
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '::1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     },
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     }
[2026-03-28 17:19:59] [FRONTEND]   ]
[2026-03-28 17:19:59] [FRONTEND] }
[2026-03-28 17:19:59] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/ocr/recent?limit=20 AggregateError [ECONNREFUSED]: 
[2026-03-28 17:19:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 17:19:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 17:19:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]   [errors]: [
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '::1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     },
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     }
[2026-03-28 17:19:59] [FRONTEND]   ]
[2026-03-28 17:19:59] [FRONTEND] }
[2026-03-28 17:19:59] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 17:19:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 17:19:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 17:19:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]   [errors]: [
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '::1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     },
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     }
[2026-03-28 17:19:59] [FRONTEND]   ]
[2026-03-28 17:19:59] [FRONTEND] }
[2026-03-28 17:19:59] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 17:19:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 17:19:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 17:19:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]   [errors]: [
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '::1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     },
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     }
[2026-03-28 17:19:59] [FRONTEND]   ]
[2026-03-28 17:19:59] [FRONTEND] }
[2026-03-28 17:19:59] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 17:19:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 17:19:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 17:19:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]   [errors]: [
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '::1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     },
[2026-03-28 17:19:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 17:19:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 17:19:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 17:19:59] [FRONTEND]       errno: -61,
[2026-03-28 17:19:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 17:19:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 17:19:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 17:19:59] [FRONTEND]       port: 5001
[2026-03-28 17:19:59] [FRONTEND]     }
[2026-03-28 17:19:59] [FRONTEND]   ]
[2026-03-28 17:19:59] [FRONTEND] }
[2026-03-28 17:19:59] [FRONTEND]  ✓ Compiled /_error in 376ms (259 modules)
[2026-03-28 17:20:02] [DOCLING] 2026-03-28 17:20:02,393 - INFO - DocumentConverter initialized in 6.20s
[2026-03-28 17:20:02] [DOCLING] INFO:     Application startup complete.
[2026-03-28 17:20:02] [DOCLING] ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 5002): address already in use
[2026-03-28 17:20:02] [DOCLING] INFO:     Waiting for application shutdown.
[2026-03-28 17:20:02] [DOCLING] INFO:     Application shutdown complete.
[2026-03-28 17:20:03] [DOCLING] cd backend && opendataloader-pdf-hybrid --port 5002 exited with code 1
[2026-03-28 17:20:03] [CELERY]  
[2026-03-28 17:20:03] [CELERY]  -------------- celery@192.168.1.8 v5.3.4 (emerald-rush)
[2026-03-28 17:20:03] [CELERY] --- ***** ----- 
[2026-03-28 17:20:03] [CELERY] -- ******* ---- macOS-26.3.1-arm64-arm-64bit 2026-03-28 17:20:03
[2026-03-28 17:20:03] [CELERY] - *** --- * --- 
[2026-03-28 17:20:03] [CELERY] - ** ---------- [config]
[2026-03-28 17:20:03] [CELERY] - ** ---------- .> app:         worker:0x1077aa170
[2026-03-28 17:20:03] [CELERY] - ** ---------- .> transport:   redis://localhost:6379/0
[2026-03-28 17:20:03] [CELERY] - ** ---------- .> results:     redis://localhost:6379/0
[2026-03-28 17:20:03] [CELERY] - *** --- * --- .> concurrency: 8 (solo)
[2026-03-28 17:20:03] [CELERY] -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
[2026-03-28 17:20:03] [CELERY] --- ***** ----- 
[2026-03-28 17:20:03] [CELERY]  -------------- [queues]
[2026-03-28 17:20:03] [CELERY]                 .> celery           exchange=celery(direct) key=celery
[2026-03-28 17:20:03] [CELERY]                 
[2026-03-28 17:20:03] [CELERY] 
[2026-03-28 17:20:03] [CELERY] [tasks]
[2026-03-28 17:20:03] [CELERY]   . app.tasks.ocr_tasks.run_historical_ocr_backfill
[2026-03-28 17:20:03] [CELERY]   . app.tasks.scraping_tasks.run_scraping_task
[2026-03-28 17:20:03] [CELERY] 
[2026-03-28 17:20:03] [CELERY] 2026-03-28 17:20:03,673 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 17:20:03] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 17:20:03] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 17:20:03] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 17:20:03] [CELERY]   warnings.warn(
[2026-03-28 17:20:03] [CELERY] 
[2026-03-28 17:20:03] [CELERY] 2026-03-28 17:20:03,677 - celery.worker.consumer.connection - INFO - Connected to redis://localhost:6379/0
[2026-03-28 17:20:03] [CELERY] 2026-03-28 17:20:03,677 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 17:20:03] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 17:20:03] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 17:20:03] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 17:20:03] [CELERY]   warnings.warn(
[2026-03-28 17:20:03] [CELERY] 
[2026-03-28 17:20:03] [CELERY] 2026-03-28 17:20:03,678 - celery.worker.consumer.mingle - INFO - mingle: searching for neighbors
[2026-03-28 17:20:04] [CELERY] 2026-03-28 17:20:04,683 - celery.worker.consumer.mingle - INFO - mingle: all alone
[2026-03-28 17:20:04] [CELERY] 2026-03-28 17:20:04,690 - celery.apps.worker - INFO - celery@192.168.1.8 ready.
[2026-03-28 17:20:06] [BACKEND] INFO:     Started server process [93347]
[2026-03-28 17:20:06] [BACKEND] INFO:     Waiting for application startup.
[2026-03-28 17:20:07] [BACKEND] INFO:     Application startup complete.
[2026-03-28 17:20:07] [BACKEND] INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
[2026-03-28 17:21:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:22:07] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:22:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:24:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:24:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:26:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:26:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:27:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:29:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:30:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:31:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:32:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:33:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:34:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:34:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:36:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:37:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:38:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:39:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:40:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:41:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:42:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:43:03] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:44:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:44:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:46:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:47:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:48:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:49:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:49:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:51:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:52:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:53:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:54:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:55:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:56:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:57:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:58:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 17:59:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:00:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:01:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:02:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:02:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:04:08] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:05:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:05:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:07:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:08:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:09:09] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:10:18] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:11:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:12:05] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:13:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:14:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:15:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:16:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:16:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:18:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 18:19:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa


---
**YENİ OTURUM BAŞLADI:** Sat Mar 28 18:54:36 +03 2026
---

[2026-03-28 18:54:37] [BACKEND] >>> Sicilius Backend Startup Sequence Initiated <<<
[2026-03-28 18:54:37] [FRONTEND] yarn run v1.22.22
[2026-03-28 18:54:37] [FRONTEND] $ next dev
[2026-03-28 18:54:37] [BACKEND] [+] Eski (zombi) SSH tüneli bulundu, temizleniyor...
[2026-03-28 18:54:38] [FRONTEND]   ▲ Next.js 14.2.3
[2026-03-28 18:54:38] [FRONTEND]   - Local:        http://localhost:3000
[2026-03-28 18:54:38] [FRONTEND]   - Environments: .env.local
[2026-03-28 18:54:38] [FRONTEND] 
[2026-03-28 18:54:38] [FRONTEND]  ✓ Starting...
[2026-03-28 18:54:38] [DOCLING] 2026-03-28 18:54:38,649 - INFO - No GPU detected, using CPU.
[2026-03-28 18:54:38] [DOCLING] 2026-03-28 18:54:38,649 - INFO - Starting Docling Fast Server on http://0.0.0.0:5002
[2026-03-28 18:54:38] [DOCLING] 2026-03-28 18:54:38,649 - INFO - OCR settings: force_ocr=False, lang=default
[2026-03-28 18:54:38] [DOCLING] INFO:     Started server process [62113]
[2026-03-28 18:54:38] [DOCLING] INFO:     Waiting for application startup.
[2026-03-28 18:54:38] [DOCLING] 2026-03-28 18:54:38,683 - INFO - Initializing DocumentConverter (force_ocr=False, lang=default, enrichments=none)...
[2026-03-28 18:54:38] [BACKEND] [+] Yeni SSH database tüneli kuruluyor. Uzak veritabanı IP'si bulunuyor...
[2026-03-28 18:54:40] [FRONTEND]  ✓ Ready in 1976ms
[2026-03-28 18:54:41] [BACKEND] [+] Remote database IP found: 172.18.0.6. Establishing tunnel...
[2026-03-28 18:54:41] [BACKEND] bind [127.0.0.1]:9000: Address already in use
[2026-03-28 18:54:41] [BACKEND] channel_setup_fwd_listener_tcpip: cannot listen to port: 9000
[2026-03-28 18:54:41] [BACKEND] [+] SSH Tunnel successfully established to 172.18.0.6.
[2026-03-28 18:54:41] [BACKEND] [+] Starting FastAPI server...
[2026-03-28 18:54:44] [DOCLING] 2026-03-28 18:54:44,806 - INFO - DocumentConverter initialized in 6.12s
[2026-03-28 18:54:44] [DOCLING] INFO:     Application startup complete.
[2026-03-28 18:54:44] [DOCLING] ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 5002): address already in use
[2026-03-28 18:54:44] [DOCLING] INFO:     Waiting for application shutdown.
[2026-03-28 18:54:44] [DOCLING] INFO:     Application shutdown complete.
[2026-03-28 18:54:45] [DOCLING] cd backend && opendataloader-pdf-hybrid --port 5002 exited with code 1
[2026-03-28 18:54:46] [CELERY]  
[2026-03-28 18:54:46] [CELERY]  -------------- celery@192.168.1.8 v5.3.4 (emerald-rush)
[2026-03-28 18:54:46] [CELERY] --- ***** ----- 
[2026-03-28 18:54:46] [CELERY] -- ******* ---- macOS-26.3.1-arm64-arm-64bit 2026-03-28 18:54:46
[2026-03-28 18:54:46] [CELERY] - *** --- * --- 
[2026-03-28 18:54:46] [CELERY] - ** ---------- [config]
[2026-03-28 18:54:46] [CELERY] - ** ---------- .> app:         worker:0x10b296140
[2026-03-28 18:54:46] [CELERY] - ** ---------- .> transport:   redis://localhost:6379/0
[2026-03-28 18:54:46] [CELERY] - ** ---------- .> results:     redis://localhost:6379/0
[2026-03-28 18:54:46] [CELERY] - *** --- * --- .> concurrency: 8 (solo)
[2026-03-28 18:54:46] [CELERY] -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
[2026-03-28 18:54:46] [CELERY] --- ***** ----- 
[2026-03-28 18:54:46] [CELERY]  -------------- [queues]
[2026-03-28 18:54:46] [CELERY]                 .> celery           exchange=celery(direct) key=celery
[2026-03-28 18:54:46] [CELERY]                 
[2026-03-28 18:54:46] [CELERY] 
[2026-03-28 18:54:46] [CELERY] [tasks]
[2026-03-28 18:54:46] [CELERY]   . app.tasks.ocr_tasks.run_historical_ocr_backfill
[2026-03-28 18:54:46] [CELERY]   . app.tasks.scraping_tasks.run_scraping_task
[2026-03-28 18:54:46] [CELERY] 
[2026-03-28 18:54:46] [CELERY] 2026-03-28 18:54:46,085 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 18:54:46] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 18:54:46] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 18:54:46] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 18:54:46] [CELERY]   warnings.warn(
[2026-03-28 18:54:46] [CELERY] 
[2026-03-28 18:54:46] [CELERY] 2026-03-28 18:54:46,089 - celery.worker.consumer.connection - INFO - Connected to redis://localhost:6379/0
[2026-03-28 18:54:46] [CELERY] 2026-03-28 18:54:46,089 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 18:54:46] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 18:54:46] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 18:54:46] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 18:54:46] [CELERY]   warnings.warn(
[2026-03-28 18:54:46] [CELERY] 
[2026-03-28 18:54:46] [CELERY] 2026-03-28 18:54:46,090 - celery.worker.consumer.mingle - INFO - mingle: searching for neighbors
[2026-03-28 18:54:47] [CELERY] 2026-03-28 18:54:47,133 - celery.worker.consumer.mingle - INFO - mingle: all alone
[2026-03-28 18:54:47] [CELERY] 2026-03-28 18:54:47,140 - celery.apps.worker - INFO - celery@192.168.1.8 ready.
[2026-03-28 18:54:48] [BACKEND] INFO:     Started server process [62163]
[2026-03-28 18:54:48] [BACKEND] INFO:     Waiting for application startup.
[2026-03-28 18:54:50] [BACKEND] INFO:     Application startup complete.
[2026-03-28 18:54:50] [BACKEND] INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
[2026-03-28 19:20:06] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:21:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:21:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:23:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:24:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:25:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:26:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:27:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:28:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:29:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:30:25] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:31:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:32:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:33:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:34:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:35:15] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:36:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:36:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:38:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:38:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:40:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa


---
**YENİ OTURUM BAŞLADI:** Sat Mar 28 19:43:46 +03 2026
---

[2026-03-28 19:43:47] [BACKEND] >>> Sicilius Backend Startup Sequence Initiated <<<
[2026-03-28 19:43:47] [BACKEND] [+] Eski (zombi) SSH tüneli bulundu, temizleniyor...
[2026-03-28 19:43:47] [FRONTEND] yarn run v1.22.22
[2026-03-28 19:43:47] [FRONTEND] $ next dev
[2026-03-28 19:43:48] [FRONTEND]   ▲ Next.js 14.2.3
[2026-03-28 19:43:48] [FRONTEND]   - Local:        http://localhost:3000
[2026-03-28 19:43:48] [FRONTEND]   - Environments: .env.local
[2026-03-28 19:43:48] [FRONTEND] 
[2026-03-28 19:43:48] [FRONTEND]  ✓ Starting...
[2026-03-28 19:43:49] [DOCLING] 2026-03-28 19:43:49,025 - INFO - No GPU detected, using CPU.
[2026-03-28 19:43:49] [DOCLING] 2026-03-28 19:43:49,025 - INFO - Starting Docling Fast Server on http://0.0.0.0:5002
[2026-03-28 19:43:49] [DOCLING] 2026-03-28 19:43:49,025 - INFO - OCR settings: force_ocr=False, lang=default
[2026-03-28 19:43:49] [BACKEND] [+] Yeni SSH database tüneli kuruluyor. Uzak veritabanı IP'si bulunuyor...
[2026-03-28 19:43:49] [DOCLING] INFO:     Started server process [82389]
[2026-03-28 19:43:49] [DOCLING] INFO:     Waiting for application startup.
[2026-03-28 19:43:49] [DOCLING] 2026-03-28 19:43:49,063 - INFO - Initializing DocumentConverter (force_ocr=False, lang=default, enrichments=none)...
[2026-03-28 19:43:50] [FRONTEND]  ✓ Ready in 1934ms
[2026-03-28 19:43:51] [BACKEND] [+] Remote database IP found: 172.18.0.6. Establishing tunnel...
[2026-03-28 19:43:51] [BACKEND] bind [127.0.0.1]:9000: Address already in use
[2026-03-28 19:43:51] [BACKEND] channel_setup_fwd_listener_tcpip: cannot listen to port: 9000
[2026-03-28 19:43:51] [BACKEND] [+] SSH Tunnel successfully established to 172.18.0.6.
[2026-03-28 19:43:51] [BACKEND] [+] Starting FastAPI server...
[2026-03-28 19:43:55] [DOCLING] 2026-03-28 19:43:55,290 - INFO - DocumentConverter initialized in 6.23s
[2026-03-28 19:43:55] [DOCLING] INFO:     Application startup complete.
[2026-03-28 19:43:55] [DOCLING] ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 5002): address already in use
[2026-03-28 19:43:55] [DOCLING] INFO:     Waiting for application shutdown.
[2026-03-28 19:43:55] [DOCLING] INFO:     Application shutdown complete.
[2026-03-28 19:43:56] [DOCLING] cd backend && opendataloader-pdf-hybrid --port 5002 exited with code 1
[2026-03-28 19:43:56] [CELERY]  
[2026-03-28 19:43:56] [CELERY]  -------------- celery@192.168.1.8 v5.3.4 (emerald-rush)
[2026-03-28 19:43:56] [CELERY] --- ***** ----- 
[2026-03-28 19:43:56] [CELERY] -- ******* ---- macOS-26.3.1-arm64-arm-64bit 2026-03-28 19:43:56
[2026-03-28 19:43:56] [CELERY] - *** --- * --- 
[2026-03-28 19:43:56] [CELERY] - ** ---------- [config]
[2026-03-28 19:43:56] [CELERY] - ** ---------- .> app:         worker:0x107d8a140
[2026-03-28 19:43:56] [CELERY] - ** ---------- .> transport:   redis://localhost:6379/0
[2026-03-28 19:43:56] [CELERY] - ** ---------- .> results:     redis://localhost:6379/0
[2026-03-28 19:43:56] [CELERY] - *** --- * --- .> concurrency: 8 (solo)
[2026-03-28 19:43:56] [CELERY] -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
[2026-03-28 19:43:56] [CELERY] --- ***** ----- 
[2026-03-28 19:43:56] [CELERY]  -------------- [queues]
[2026-03-28 19:43:56] [CELERY]                 .> celery           exchange=celery(direct) key=celery
[2026-03-28 19:43:56] [CELERY]                 
[2026-03-28 19:43:56] [CELERY] 
[2026-03-28 19:43:56] [CELERY] [tasks]
[2026-03-28 19:43:56] [CELERY]   . app.tasks.ocr_tasks.run_historical_ocr_backfill
[2026-03-28 19:43:56] [CELERY]   . app.tasks.scraping_tasks.run_scraping_task
[2026-03-28 19:43:56] [CELERY] 
[2026-03-28 19:43:56] [CELERY] 2026-03-28 19:43:56,614 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 19:43:56] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 19:43:56] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 19:43:56] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 19:43:56] [CELERY]   warnings.warn(
[2026-03-28 19:43:56] [CELERY] 
[2026-03-28 19:43:56] [CELERY] 2026-03-28 19:43:56,618 - celery.worker.consumer.connection - INFO - Connected to redis://localhost:6379/0
[2026-03-28 19:43:56] [CELERY] 2026-03-28 19:43:56,618 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:507: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
[2026-03-28 19:43:56] [CELERY] whether broker connection retries are made during startup in Celery 6.0 and above.
[2026-03-28 19:43:56] [CELERY] If you wish to retain the existing behavior for retrying connections on startup,
[2026-03-28 19:43:56] [CELERY] you should set broker_connection_retry_on_startup to True.
[2026-03-28 19:43:56] [CELERY]   warnings.warn(
[2026-03-28 19:43:56] [CELERY] 
[2026-03-28 19:43:56] [CELERY] 2026-03-28 19:43:56,619 - celery.worker.consumer.mingle - INFO - mingle: searching for neighbors
[2026-03-28 19:43:57] [CELERY] 2026-03-28 19:43:57,641 - py.warnings - WARNING - /opt/homebrew/lib/python3.10/site-packages/celery/app/control.py:56: DuplicateNodenameWarning: Received multiple replies from node name: celery@192.168.1.8.
[2026-03-28 19:43:57] [CELERY] Please make sure you give each node a unique nodename using
[2026-03-28 19:43:57] [CELERY] the celery worker `-n` option.
[2026-03-28 19:43:57] [CELERY]   warnings.warn(DuplicateNodenameWarning(
[2026-03-28 19:43:57] [CELERY] 
[2026-03-28 19:43:57] [CELERY] 2026-03-28 19:43:57,641 - celery.worker.consumer.mingle - INFO - mingle: all alone
[2026-03-28 19:43:57] [CELERY] 2026-03-28 19:43:57,648 - celery.apps.worker - INFO - celery@192.168.1.8 ready.
[2026-03-28 19:43:59] [BACKEND] INFO:     Started server process [82437]
[2026-03-28 19:43:59] [BACKEND] INFO:     Waiting for application startup.
[2026-03-28 19:43:59] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/ocr/stats AggregateError [ECONNREFUSED]: 
[2026-03-28 19:43:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 19:43:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 19:43:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]   [errors]: [
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '::1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     },
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     }
[2026-03-28 19:43:59] [FRONTEND]   ]
[2026-03-28 19:43:59] [FRONTEND] }
[2026-03-28 19:43:59] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 19:43:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 19:43:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 19:43:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]   [errors]: [
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '::1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     },
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     }
[2026-03-28 19:43:59] [FRONTEND]   ]
[2026-03-28 19:43:59] [FRONTEND] }
[2026-03-28 19:43:59] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/ocr/recent?limit=20 AggregateError [ECONNREFUSED]: 
[2026-03-28 19:43:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 19:43:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 19:43:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]   [errors]: [
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '::1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     },
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     }
[2026-03-28 19:43:59] [FRONTEND]   ]
[2026-03-28 19:43:59] [FRONTEND] }
[2026-03-28 19:43:59] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 19:43:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 19:43:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 19:43:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]   [errors]: [
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '::1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     },
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     }
[2026-03-28 19:43:59] [FRONTEND]   ]
[2026-03-28 19:43:59] [FRONTEND] }
[2026-03-28 19:43:59] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me AggregateError [ECONNREFUSED]: 
[2026-03-28 19:43:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 19:43:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 19:43:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]   [errors]: [
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '::1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     },
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     }
[2026-03-28 19:43:59] [FRONTEND]   ]
[2026-03-28 19:43:59] [FRONTEND] }
[2026-03-28 19:43:59] [FRONTEND] AggregateError [ECONNREFUSED]: 
[2026-03-28 19:43:59] [FRONTEND]     at internalConnectMultiple (node:net:1122:18)
[2026-03-28 19:43:59] [FRONTEND]     at afterConnectMultiple (node:net:1689:7) {
[2026-03-28 19:43:59] [FRONTEND]   code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]   [errors]: [
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED ::1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '::1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     },
[2026-03-28 19:43:59] [FRONTEND]     Error: connect ECONNREFUSED 127.0.0.1:5001
[2026-03-28 19:43:59] [FRONTEND]         at createConnectionError (node:net:1652:14)
[2026-03-28 19:43:59] [FRONTEND]         at afterConnectMultiple (node:net:1682:16) {
[2026-03-28 19:43:59] [FRONTEND]       errno: -61,
[2026-03-28 19:43:59] [FRONTEND]       code: 'ECONNREFUSED',
[2026-03-28 19:43:59] [FRONTEND]       syscall: 'connect',
[2026-03-28 19:43:59] [FRONTEND]       address: '127.0.0.1',
[2026-03-28 19:43:59] [FRONTEND]       port: 5001
[2026-03-28 19:43:59] [FRONTEND]     }
[2026-03-28 19:43:59] [FRONTEND]   ]
[2026-03-28 19:43:59] [FRONTEND] }
[2026-03-28 19:43:59] [FRONTEND]  ✓ Compiled /_error in 235ms (259 modules)
[2026-03-28 19:44:00] [BACKEND] INFO:     Application startup complete.
[2026-03-28 19:44:00] [BACKEND] INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
[2026-03-28 19:45:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:45:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:47:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:48:01] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:49:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:50:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:51:11] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:52:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:52:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:54:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:54:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:56:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:57:11] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:57:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 19:59:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:00:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:01:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:02:22] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:03:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:04:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:05:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:06:02] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:06:59] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:08:00] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:15:43] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me Error: socket hang up
[2026-03-28 20:15:43] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 20:15:43] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 20:15:43] [FRONTEND]     at TCP.<anonymous> (node:net:343:12) {
[2026-03-28 20:15:43] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 20:15:43] [FRONTEND] }
[2026-03-28 20:15:43] [FRONTEND] Error: socket hang up
[2026-03-28 20:15:43] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 20:15:43] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 20:15:43] [FRONTEND]     at TCP.<anonymous> (node:net:343:12) {
[2026-03-28 20:15:43] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 20:15:43] [FRONTEND] }
[2026-03-28 20:16:43] [FRONTEND] Failed to proxy http://localhost:5001/api/v1/usage/me Error: socket hang up
[2026-03-28 20:16:43] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 20:16:43] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 20:16:43] [FRONTEND]     at TCP.<anonymous> (node:net:343:12) {
[2026-03-28 20:16:43] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 20:16:43] [FRONTEND] }
[2026-03-28 20:16:43] [FRONTEND] Error: socket hang up
[2026-03-28 20:16:43] [FRONTEND]     at Socket.socketCloseListener (node:_http_client:477:27)
[2026-03-28 20:16:43] [FRONTEND]     at Socket.emit (node:events:530:35)
[2026-03-28 20:16:43] [FRONTEND]     at TCP.<anonymous> (node:net:343:12) {
[2026-03-28 20:16:43] [FRONTEND]   code: 'ECONNRESET'
[2026-03-28 20:16:43] [FRONTEND] }
[2026-03-28 20:16:44] [BACKEND] ERROR:    Exception in ASGI application
[2026-03-28 20:16:44] [BACKEND] Traceback (most recent call last):
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
[2026-03-28 20:16:44] [BACKEND]     self._dbapi_connection = engine.raw_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3292, in raw_connection
[2026-03-28 20:16:44] [BACKEND]     return self.pool.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
[2026-03-28 20:16:44] [BACKEND]     return _ConnectionFairy._checkout(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1269, in _checkout
[2026-03-28 20:16:44] [BACKEND]     fairy = _ConnectionRecord.checkout(pool)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 721, in checkout
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 719, in checkout
[2026-03-28 20:16:44] [BACKEND]     dbapi_connection = rec.get_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in get_connection
[2026-03-28 20:16:44] [BACKEND]     self.__connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
[2026-03-28 20:16:44] [BACKEND]     self.dbapi_connection = connection = pool._invoke_creator(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
[2026-03-28 20:16:44] [BACKEND]     return dialect.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 616, in connect
[2026-03-28 20:16:44] [BACKEND]     return self.loaded_dbapi.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
[2026-03-28 20:16:44] [BACKEND]     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
[2026-03-28 20:16:44] [BACKEND] psycopg2.OperationalError: connection to server at "localhost" (::1), port 5433 failed: server closed the connection unexpectedly
[2026-03-28 20:16:44] [BACKEND] 	This probably means the server terminated abnormally
[2026-03-28 20:16:44] [BACKEND] 	before or while processing the request.
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] The above exception was the direct cause of the following exception:
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] Traceback (most recent call last):
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/protocols/http/httptools_impl.py", line 435, in run_asgi
[2026-03-28 20:16:44] [BACKEND]     result = await app(  # type: ignore[func-returns-value]
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
[2026-03-28 20:16:44] [BACKEND]     return await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/applications.py", line 1106, in __call__
[2026-03-28 20:16:44] [BACKEND]     await super().__call__(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/applications.py", line 122, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.middleware_stack(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/errors.py", line 184, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/errors.py", line 162, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, _send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/cors.py", line 83, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/sessions.py", line 86, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send_wrapper)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 108, in __call__
[2026-03-28 20:16:44] [BACKEND]     response = await self.dispatch_func(request, call_next)
[2026-03-28 20:16:44] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/main.py", line 157, in log_requests
[2026-03-28 20:16:44] [BACKEND]     return await call_next(request)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 84, in call_next
[2026-03-28 20:16:44] [BACKEND]     raise app_exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 70, in coro
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive_or_disconnect, send_no_error)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
[2026-03-28 20:16:44] [BACKEND]     return await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, sender)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 20, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise e
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 17, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 718, in __call__
[2026-03-28 20:16:44] [BACKEND]     await route.handle(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 276, in handle
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 66, in app
[2026-03-28 20:16:44] [BACKEND]     response = await func(request)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/routing.py", line 264, in app
[2026-03-28 20:16:44] [BACKEND]     solved_result = await solve_dependencies(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/dependencies/utils.py", line 563, in solve_dependencies
[2026-03-28 20:16:44] [BACKEND]     solved_result = await solve_dependencies(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/dependencies/utils.py", line 594, in solve_dependencies
[2026-03-28 20:16:44] [BACKEND]     solved = await run_in_threadpool(call, **sub_values)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
[2026-03-28 20:16:44] [BACKEND]     return await anyio.to_thread.run_sync(func, *args)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/to_thread.py", line 33, in run_sync
[2026-03-28 20:16:44] [BACKEND]     return await get_asynclib().run_sync_in_worker_thread(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/_backends/_asyncio.py", line 877, in run_sync_in_worker_thread
[2026-03-28 20:16:44] [BACKEND]     return await future
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/_backends/_asyncio.py", line 807, in run
[2026-03-28 20:16:44] [BACKEND]     result = context.run(func, *args)
[2026-03-28 20:16:44] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/api/deps.py", line 76, in get_current_user
[2026-03-28 20:16:44] [BACKEND]     user = crud.user.get(db, id=token_data.sub)
[2026-03-28 20:16:44] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/crud/base.py", line 25, in get
[2026-03-28 20:16:44] [BACKEND]     return db.query(self.model).filter(self.model.id == id).first()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/query.py", line 2748, in first
[2026-03-28 20:16:44] [BACKEND]     return self.limit(1)._iter().first()  # type: ignore
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/query.py", line 2847, in _iter
[2026-03-28 20:16:44] [BACKEND]     result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2308, in execute
[2026-03-28 20:16:44] [BACKEND]     return self._execute_internal(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2180, in _execute_internal
[2026-03-28 20:16:44] [BACKEND]     conn = self._connection_for_bind(bind)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2047, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]     return trans._connection_for_bind(engine, execution_options)
[2026-03-28 20:16:44] [BACKEND]   File "<string>", line 2, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go
[2026-03-28 20:16:44] [BACKEND]     ret_value = fn(self, *arg, **kw)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1143, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]     conn = bind.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3268, in connect
[2026-03-28 20:16:44] [BACKEND]     return self._connection_cls(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 147, in __init__
[2026-03-28 20:16:44] [BACKEND]     Connection._handle_dbapi_exception_noconnection(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2430, in _handle_dbapi_exception_noconnection
[2026-03-28 20:16:44] [BACKEND]     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
[2026-03-28 20:16:44] [BACKEND]     self._dbapi_connection = engine.raw_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3292, in raw_connection
[2026-03-28 20:16:44] [BACKEND]     return self.pool.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
[2026-03-28 20:16:44] [BACKEND]     return _ConnectionFairy._checkout(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1269, in _checkout
[2026-03-28 20:16:44] [BACKEND]     fairy = _ConnectionRecord.checkout(pool)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 721, in checkout
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 719, in checkout
[2026-03-28 20:16:44] [BACKEND]     dbapi_connection = rec.get_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in get_connection
[2026-03-28 20:16:44] [BACKEND]     self.__connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
[2026-03-28 20:16:44] [BACKEND]     self.dbapi_connection = connection = pool._invoke_creator(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
[2026-03-28 20:16:44] [BACKEND]     return dialect.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 616, in connect
[2026-03-28 20:16:44] [BACKEND]     return self.loaded_dbapi.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
[2026-03-28 20:16:44] [BACKEND]     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
[2026-03-28 20:16:44] [BACKEND] sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5433 failed: server closed the connection unexpectedly
[2026-03-28 20:16:44] [BACKEND] 	This probably means the server terminated abnormally
[2026-03-28 20:16:44] [BACKEND] 	before or while processing the request.
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] (Background on this error at: https://sqlalche.me/e/20/e3q8)
[2026-03-28 20:16:44] [BACKEND] ERROR:    Exception in ASGI application
[2026-03-28 20:16:44] [BACKEND] Traceback (most recent call last):
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
[2026-03-28 20:16:44] [BACKEND]     self._dbapi_connection = engine.raw_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3292, in raw_connection
[2026-03-28 20:16:44] [BACKEND]     return self.pool.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
[2026-03-28 20:16:44] [BACKEND]     return _ConnectionFairy._checkout(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1269, in _checkout
[2026-03-28 20:16:44] [BACKEND]     fairy = _ConnectionRecord.checkout(pool)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 721, in checkout
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 719, in checkout
[2026-03-28 20:16:44] [BACKEND]     dbapi_connection = rec.get_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in get_connection
[2026-03-28 20:16:44] [BACKEND]     self.__connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
[2026-03-28 20:16:44] [BACKEND]     self.dbapi_connection = connection = pool._invoke_creator(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
[2026-03-28 20:16:44] [BACKEND]     return dialect.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 616, in connect
[2026-03-28 20:16:44] [BACKEND]     return self.loaded_dbapi.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
[2026-03-28 20:16:44] [BACKEND]     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
[2026-03-28 20:16:44] [BACKEND] psycopg2.OperationalError: connection to server at "localhost" (::1), port 5433 failed: server closed the connection unexpectedly
[2026-03-28 20:16:44] [BACKEND] 	This probably means the server terminated abnormally
[2026-03-28 20:16:44] [BACKEND] 	before or while processing the request.
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] The above exception was the direct cause of the following exception:
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] Traceback (most recent call last):
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/protocols/http/httptools_impl.py", line 435, in run_asgi
[2026-03-28 20:16:44] [BACKEND]     result = await app(  # type: ignore[func-returns-value]
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
[2026-03-28 20:16:44] [BACKEND]     return await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/applications.py", line 1106, in __call__
[2026-03-28 20:16:44] [BACKEND]     await super().__call__(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/applications.py", line 122, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.middleware_stack(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/errors.py", line 184, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/errors.py", line 162, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, _send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/cors.py", line 91, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.simple_response(scope, receive, send, request_headers=headers)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/cors.py", line 146, in simple_response
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/sessions.py", line 86, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send_wrapper)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 108, in __call__
[2026-03-28 20:16:44] [BACKEND]     response = await self.dispatch_func(request, call_next)
[2026-03-28 20:16:44] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/main.py", line 157, in log_requests
[2026-03-28 20:16:44] [BACKEND]     return await call_next(request)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 84, in call_next
[2026-03-28 20:16:44] [BACKEND]     raise app_exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 70, in coro
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive_or_disconnect, send_no_error)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
[2026-03-28 20:16:44] [BACKEND]     return await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, sender)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 20, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise e
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 17, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 718, in __call__
[2026-03-28 20:16:44] [BACKEND]     await route.handle(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 276, in handle
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 66, in app
[2026-03-28 20:16:44] [BACKEND]     response = await func(request)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/routing.py", line 274, in app
[2026-03-28 20:16:44] [BACKEND]     raw_response = await run_endpoint_function(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/routing.py", line 193, in run_endpoint_function
[2026-03-28 20:16:44] [BACKEND]     return await run_in_threadpool(dependant.call, **values)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
[2026-03-28 20:16:44] [BACKEND]     return await anyio.to_thread.run_sync(func, *args)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/to_thread.py", line 33, in run_sync
[2026-03-28 20:16:44] [BACKEND]     return await get_asynclib().run_sync_in_worker_thread(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/_backends/_asyncio.py", line 877, in run_sync_in_worker_thread
[2026-03-28 20:16:44] [BACKEND]     return await future
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/_backends/_asyncio.py", line 807, in run
[2026-03-28 20:16:44] [BACKEND]     result = context.run(func, *args)
[2026-03-28 20:16:44] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/api/api_v1/endpoints/ocr.py", line 151, in get_ocr_stats
[2026-03-28 20:16:44] [BACKEND]     db.execute(text("SET search_path TO app, public"))
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2308, in execute
[2026-03-28 20:16:44] [BACKEND]     return self._execute_internal(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2180, in _execute_internal
[2026-03-28 20:16:44] [BACKEND]     conn = self._connection_for_bind(bind)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2047, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]     return trans._connection_for_bind(engine, execution_options)
[2026-03-28 20:16:44] [BACKEND]   File "<string>", line 2, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go
[2026-03-28 20:16:44] [BACKEND]     ret_value = fn(self, *arg, **kw)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1143, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]     conn = bind.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3268, in connect
[2026-03-28 20:16:44] [BACKEND]     return self._connection_cls(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 147, in __init__
[2026-03-28 20:16:44] [BACKEND]     Connection._handle_dbapi_exception_noconnection(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2430, in _handle_dbapi_exception_noconnection
[2026-03-28 20:16:44] [BACKEND]     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
[2026-03-28 20:16:44] [BACKEND]     self._dbapi_connection = engine.raw_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3292, in raw_connection
[2026-03-28 20:16:44] [BACKEND]     return self.pool.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
[2026-03-28 20:16:44] [BACKEND]     return _ConnectionFairy._checkout(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1269, in _checkout
[2026-03-28 20:16:44] [BACKEND]     fairy = _ConnectionRecord.checkout(pool)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 721, in checkout
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 719, in checkout
[2026-03-28 20:16:44] [BACKEND]     dbapi_connection = rec.get_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in get_connection
[2026-03-28 20:16:44] [BACKEND]     self.__connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
[2026-03-28 20:16:44] [BACKEND]     self.dbapi_connection = connection = pool._invoke_creator(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
[2026-03-28 20:16:44] [BACKEND]     return dialect.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 616, in connect
[2026-03-28 20:16:44] [BACKEND]     return self.loaded_dbapi.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
[2026-03-28 20:16:44] [BACKEND]     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
[2026-03-28 20:16:44] [BACKEND] sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5433 failed: server closed the connection unexpectedly
[2026-03-28 20:16:44] [BACKEND] 	This probably means the server terminated abnormally
[2026-03-28 20:16:44] [BACKEND] 	before or while processing the request.
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] (Background on this error at: https://sqlalche.me/e/20/e3q8)
[2026-03-28 20:16:44] [BACKEND] ERROR:    Exception in ASGI application
[2026-03-28 20:16:44] [BACKEND] Traceback (most recent call last):
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
[2026-03-28 20:16:44] [BACKEND]     self._dbapi_connection = engine.raw_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3292, in raw_connection
[2026-03-28 20:16:44] [BACKEND]     return self.pool.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
[2026-03-28 20:16:44] [BACKEND]     return _ConnectionFairy._checkout(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1269, in _checkout
[2026-03-28 20:16:44] [BACKEND]     fairy = _ConnectionRecord.checkout(pool)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 721, in checkout
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 719, in checkout
[2026-03-28 20:16:44] [BACKEND]     dbapi_connection = rec.get_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in get_connection
[2026-03-28 20:16:44] [BACKEND]     self.__connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
[2026-03-28 20:16:44] [BACKEND]     self.dbapi_connection = connection = pool._invoke_creator(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
[2026-03-28 20:16:44] [BACKEND]     return dialect.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 616, in connect
[2026-03-28 20:16:44] [BACKEND]     return self.loaded_dbapi.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
[2026-03-28 20:16:44] [BACKEND]     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
[2026-03-28 20:16:44] [BACKEND] psycopg2.OperationalError: connection to server at "localhost" (::1), port 5433 failed: server closed the connection unexpectedly
[2026-03-28 20:16:44] [BACKEND] 	This probably means the server terminated abnormally
[2026-03-28 20:16:44] [BACKEND] 	before or while processing the request.
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] The above exception was the direct cause of the following exception:
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] Traceback (most recent call last):
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/protocols/http/httptools_impl.py", line 435, in run_asgi
[2026-03-28 20:16:44] [BACKEND]     result = await app(  # type: ignore[func-returns-value]
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
[2026-03-28 20:16:44] [BACKEND]     return await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/applications.py", line 1106, in __call__
[2026-03-28 20:16:44] [BACKEND]     await super().__call__(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/applications.py", line 122, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.middleware_stack(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/errors.py", line 184, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/errors.py", line 162, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, _send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/cors.py", line 91, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.simple_response(scope, receive, send, request_headers=headers)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/cors.py", line 146, in simple_response
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/sessions.py", line 86, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send_wrapper)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 108, in __call__
[2026-03-28 20:16:44] [BACKEND]     response = await self.dispatch_func(request, call_next)
[2026-03-28 20:16:44] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/main.py", line 157, in log_requests
[2026-03-28 20:16:44] [BACKEND]     return await call_next(request)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 84, in call_next
[2026-03-28 20:16:44] [BACKEND]     raise app_exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/base.py", line 70, in coro
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive_or_disconnect, send_no_error)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
[2026-03-28 20:16:44] [BACKEND]     return await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise exc
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, sender)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 20, in __call__
[2026-03-28 20:16:44] [BACKEND]     raise e
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 17, in __call__
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 718, in __call__
[2026-03-28 20:16:44] [BACKEND]     await route.handle(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 276, in handle
[2026-03-28 20:16:44] [BACKEND]     await self.app(scope, receive, send)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/routing.py", line 66, in app
[2026-03-28 20:16:44] [BACKEND]     response = await func(request)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/routing.py", line 274, in app
[2026-03-28 20:16:44] [BACKEND]     raw_response = await run_endpoint_function(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/fastapi/routing.py", line 193, in run_endpoint_function
[2026-03-28 20:16:44] [BACKEND]     return await run_in_threadpool(dependant.call, **values)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
[2026-03-28 20:16:44] [BACKEND]     return await anyio.to_thread.run_sync(func, *args)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/to_thread.py", line 33, in run_sync
[2026-03-28 20:16:44] [BACKEND]     return await get_asynclib().run_sync_in_worker_thread(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/_backends/_asyncio.py", line 877, in run_sync_in_worker_thread
[2026-03-28 20:16:44] [BACKEND]     return await future
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/anyio/_backends/_asyncio.py", line 807, in run
[2026-03-28 20:16:44] [BACKEND]     result = context.run(func, *args)
[2026-03-28 20:16:44] [BACKEND]   File "/Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/backend/app/api/api_v1/endpoints/ocr.py", line 187, in get_recent_ocr_results
[2026-03-28 20:16:44] [BACKEND]     db.execute(text("SET search_path TO app, public"))
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2308, in execute
[2026-03-28 20:16:44] [BACKEND]     return self._execute_internal(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2180, in _execute_internal
[2026-03-28 20:16:44] [BACKEND]     conn = self._connection_for_bind(bind)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2047, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]     return trans._connection_for_bind(engine, execution_options)
[2026-03-28 20:16:44] [BACKEND]   File "<string>", line 2, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go
[2026-03-28 20:16:44] [BACKEND]     ret_value = fn(self, *arg, **kw)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1143, in _connection_for_bind
[2026-03-28 20:16:44] [BACKEND]     conn = bind.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3268, in connect
[2026-03-28 20:16:44] [BACKEND]     return self._connection_cls(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 147, in __init__
[2026-03-28 20:16:44] [BACKEND]     Connection._handle_dbapi_exception_noconnection(
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2430, in _handle_dbapi_exception_noconnection
[2026-03-28 20:16:44] [BACKEND]     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
[2026-03-28 20:16:44] [BACKEND]     self._dbapi_connection = engine.raw_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3292, in raw_connection
[2026-03-28 20:16:44] [BACKEND]     return self.pool.connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
[2026-03-28 20:16:44] [BACKEND]     return _ConnectionFairy._checkout(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1269, in _checkout
[2026-03-28 20:16:44] [BACKEND]     fairy = _ConnectionRecord.checkout(pool)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 721, in checkout
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 719, in checkout
[2026-03-28 20:16:44] [BACKEND]     dbapi_connection = rec.get_connection()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in get_connection
[2026-03-28 20:16:44] [BACKEND]     self.__connect()
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
[2026-03-28 20:16:44] [BACKEND]     with util.safe_reraise():
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
[2026-03-28 20:16:44] [BACKEND]     raise exc_value.with_traceback(exc_tb)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
[2026-03-28 20:16:44] [BACKEND]     self.dbapi_connection = connection = pool._invoke_creator(self)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
[2026-03-28 20:16:44] [BACKEND]     return dialect.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 616, in connect
[2026-03-28 20:16:44] [BACKEND]     return self.loaded_dbapi.connect(*cargs, **cparams)
[2026-03-28 20:16:44] [BACKEND]   File "/opt/homebrew/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
[2026-03-28 20:16:44] [BACKEND]     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
[2026-03-28 20:16:44] [BACKEND] sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5433 failed: server closed the connection unexpectedly
[2026-03-28 20:16:44] [BACKEND] 	This probably means the server terminated abnormally
[2026-03-28 20:16:44] [BACKEND] 	before or while processing the request.
[2026-03-28 20:16:44] [BACKEND] 
[2026-03-28 20:16:44] [BACKEND] (Background on this error at: https://sqlalche.me/e/20/e3q8)
[2026-03-28 20:16:44] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:17:21] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:19:19] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:20:50] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:23:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:24:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:25:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:26:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:27:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:28:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:29:43] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:30:41] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:31:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:32:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:33:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:34:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:35:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:36:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:37:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:38:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:39:48] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:40:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:41:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:42:41] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:43:40] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 20:44:41] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:00:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:01:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:02:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:04:04] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:04:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:05:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:06:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:08:12] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:08:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
[2026-03-28 21:09:54] [BACKEND] DEBUG: usage/me for user_id=b03a99e6-69eb-4266-affb-2b855737d9aa
