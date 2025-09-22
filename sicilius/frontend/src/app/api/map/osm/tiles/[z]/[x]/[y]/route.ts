import { NextResponse } from 'next/server';

export const runtime = 'nodejs';

export async function GET(
  _req: Request,
  { params }: { params: { z: string; x: string; y: string } }
) {
  const { z, x } = params;
  const yRaw = params.y || '';
  const y = yRaw.replace(/\.png$/i, '');

  // Use single-origin OSM tile endpoint to avoid cross-origin/COEP issues
  // Policy: For production, please cache and throttle respectfully.
  const upstream = `https://tile.openstreetmap.org/${encodeURIComponent(z)}/${encodeURIComponent(x)}/${encodeURIComponent(y)}.png`;

  try {
    const res = await fetch(upstream, {
      cache: 'force-cache',
      headers: {
        'Accept': 'image/png',
        // Set a user agent to be polite to OSM tile servers
        'User-Agent': 'Sicilius/1.0 (+https://example.local)'
      },
    });

    if (!res.ok) {
      return NextResponse.json({ error: 'OSM upstream tile fetch failed', status: res.status }, { status: res.status });
    }

    const buff = Buffer.from(await res.arrayBuffer());
    return new NextResponse(buff, {
      headers: {
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=86400, s-maxage=86400, immutable',
      },
    });
  } catch (err) {
    return NextResponse.json({ error: 'OSM tile proxy error', detail: (err as Error).message }, { status: 502 });
  }
}
