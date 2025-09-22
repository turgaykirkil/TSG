import { NextResponse } from 'next/server';

export const runtime = 'nodejs';

export async function GET(
  _req: Request,
  { params }: { params: { z: string; x: string; y: string } }
) {
  const { z, x } = params;
  // y gelebilir: "1234" ya da "1234.png" — uzantıyı temizle
  const yRaw = params.y || '';
  const y = yRaw.replace(/\.png$/i, '');
  // Server-side token: do NOT prefix with NEXT_PUBLIC_
  const token = process.env.TSG_LOCATIONIQ_TOKEN
    || process.env.LOCATIONIQ_TOKEN
    || process.env.LOCATIONIQ_API_KEY;

  if (!token) {
    return NextResponse.json({ error: 'Server-side LocationIQ token is not configured' }, { status: 500 });
  }

  // LocationIQ raster tiles endpoint (PNG)
  const upstream = `https://tiles.locationiq.com/v3/streets/${encodeURIComponent(z)}/${encodeURIComponent(x)}/${encodeURIComponent(y)}.png?key=${encodeURIComponent(token)}`;

  try {
    const res = await fetch(upstream, {
      // cache tiles aggressively at the edge/node runtime
      cache: 'force-cache',
      headers: {
        // accept png
        'Accept': 'image/png',
      },
    });

    if (!res.ok) {
      return NextResponse.json({ error: 'Upstream tile fetch failed', status: res.status }, { status: res.status });
    }

    const buff = Buffer.from(await res.arrayBuffer());
    return new NextResponse(buff, {
      headers: {
        'Content-Type': 'image/png',
        // 1 day cache; adjust as needed
        'Cache-Control': 'public, max-age=86400, s-maxage=86400, immutable',
      },
    });
  } catch (err) {
    return NextResponse.json({ error: 'Tile proxy error', detail: (err as Error).message }, { status: 502 });
  }
}
