import { NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';

// Proxy endpoint to check session status from scraping backend
export async function GET(req: Request) {
  try {
    const backendUrl = process.env.SCRAPING_BACKEND_URL ?? 'http://localhost:5001';
    const cookie = req.headers.get('cookie') || '';
    const res = await fetch(`${backendUrl}/session`, {
      method: 'GET',
      headers: { cookie }
    });
    if (!res.ok) throw new Error(`Backend returned ${res.status}`);
    const data = await res.json();
    return NextResponse.json({ loggedIn: data.loggedIn });
  } catch (err) {
    console.error('[api/scraping/session]', err);
    return NextResponse.json({ error: 'Session fetch failed' }, { status: 500 });
  }
}
