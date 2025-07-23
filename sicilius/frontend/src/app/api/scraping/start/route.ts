import { NextResponse } from 'next/server';

// Proxy endpoint to start scraping via backend service
export async function POST(req: Request) {
  try {
    const backendUrl = process.env.SCRAPING_BACKEND_URL ?? 'http://localhost:5001';
    // Forward session cookie for authenticated scraping
    const cookie = req.headers.get('cookie') || '';
    const res = await fetch(`${backendUrl}/start`, {
      method: 'POST',
      headers: { cookie },
    });
    if (!res.ok) throw new Error(`Backend returned ${res.status}`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err) {
    console.error('[api/scraping/start]', err);
    return NextResponse.json({ error: 'Scraping başlatma başarısız' }, { status: 500 });
  }
}
