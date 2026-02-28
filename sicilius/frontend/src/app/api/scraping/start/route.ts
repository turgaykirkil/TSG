import { NextResponse } from 'next/server';

// Helper to check backend health status
const checkHealth = async (host: string, port: number) => {
  try {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 2000); // 2s ping timeout
    const res = await fetch(`http://${host}:${port}/api/health`, {
      method: 'GET',
      signal: controller.signal
    });
    clearTimeout(id);
    return res.ok;
  } catch (e) {
    return false;
  }
};

// Proxy endpoint to start scraping via backend service
export async function POST(req: Request) {
  const primaryHost = 'localhost';
  const primaryPort = 5002;

  const secondaryHost = 'localhost';
  const secondaryPort = 5001;

  const cookie = req.headers.get('cookie') || '';

  // 1. Determine Target Backend
  // 1. Determine Target Backend
  const body = await req.json().catch(() => ({}));
  const workerSource = body.worker_source; // 'local' | 'remote' | undefined

  let targetHost: string | null = null;
  let targetPort: number | null = null;

  console.log(`[api/scraping/start] Worker Source Request: ${workerSource || 'AUTO'}`);

  if (workerSource === 'remote') {
    // Force Remote (Old Mac via Tunnel)
    targetHost = primaryHost;
    targetPort = primaryPort;
    console.log(`[api/scraping/start] Forcing REMOTE worker (${targetHost}:${targetPort})`);
  } else if (workerSource === 'local') {
    // Force Local (Docker)
    targetHost = secondaryHost;
    targetPort = secondaryPort;
    console.log(`[api/scraping/start] Forcing LOCAL worker (${targetHost}:${targetPort})`);
  } else {
    // Default: Auto Failover (Priority: Remote > Local)
    // Check Primary (Remote 5002)
    console.log(`[api/scraping/start] Checking health of Primary ${primaryHost}:${primaryPort}...`);
    if (await checkHealth(primaryHost, primaryPort)) {
      targetHost = primaryHost;
      targetPort = primaryPort;
      console.log(`[api/scraping/start] Primary ${primaryHost}:${primaryPort} is HEALTHY. Using Primary.`);
    } else {
      console.warn(`[api/scraping/start] Primary ${primaryHost}:${primaryPort} is UNREACHABLE. Checking Secondary...`);
      // Check Secondary (Local 5001)
      if (await checkHealth(secondaryHost, secondaryPort)) {
        targetHost = secondaryHost;
        targetPort = secondaryPort;
        console.log(`[api/scraping/start] Secondary ${secondaryHost}:${secondaryPort} is HEALTHY. Using Secondary.`);
      }
    }
  }

  if (!targetHost || !targetPort) {
    console.error('[api/scraping/start] No working backend found.');
    return NextResponse.json({ error: 'Hiçbir scraping servisine erişilemedi (Uzak 5002 ve Yerel 5001 kapalı).' }, { status: 503 });
  }

  // 2. Perform Request to Target
  // We use a much longer timeout for the actual operation to allow browser startup
  const targetUrl = `http://${targetHost}:${targetPort}/api/v1/scraping/start`;
  const timeout = 60000; // 60 seconds timeout for operation start

  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    console.log(`[api/scraping/start] Sending request to ${targetUrl}...`);
    // body is already parsed above


    const res = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        cookie,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body),
      signal: controller.signal
    });

    clearTimeout(id);

    if (!res.ok) {
      const text = await res.text();
      console.error(`[api/scraping/start] Target ${targetPort} returned error: ${res.status} ${text}`);
      throw new Error(`Scraping service error: ${res.status}`);
    }

    const data = await res.json();
    return NextResponse.json(data);

  } catch (err: any) {
    clearTimeout(id);
    console.error(`[api/scraping/start] Error during request to ${targetPort}:`, err);

    // Detect duplication/timeout specific errors
    if (err.name === 'AbortError') {
      return NextResponse.json({ error: 'İstek zaman aşımına uğradı (Browser açılması uzun sürdü), ancak işlem arka planda başlamış olabilir.' }, { status: 504 });
    }

    return NextResponse.json({ error: `Scraping başlatılamadı: ${err.message}` }, { status: 500 });
  }
}
