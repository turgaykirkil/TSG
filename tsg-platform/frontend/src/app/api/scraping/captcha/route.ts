import { NextResponse } from 'next/server';

// Proxy endpoint to fetch CAPTCHA image from scraping backend
export async function GET() {
  try {
    const backendUrl = process.env.SCRAPING_BACKEND_URL ?? 'http://localhost:5001';
    if (!backendUrl) throw new Error('SCRAPING_BACKEND_URL not defined');

    const res = await fetch(`${backendUrl}/captcha`, { cache: 'no-store' });
    if (!res.ok) throw new Error(`Backend returned ${res.status}`);
    const data = await res.json();

    return NextResponse.json({ image: data.image });
  } catch (err) {
    console.error('[api/captcha]', err);
    return NextResponse.json({ error: 'Captcha fetch failed' }, { status: 500 });
  }
}
