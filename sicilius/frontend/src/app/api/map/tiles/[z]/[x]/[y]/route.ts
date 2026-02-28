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

  // Fallback function for OSM
  const serveOsm = async () => {
    // OSM requires a valid User-Agent
    const osmUpstream = `https://tile.openstreetmap.org/${z}/${x}/${y}.png`;
    console.log(`[TileProxy] Fallback to OSM: ${osmUpstream}`);
    try {
      const resp = await fetch(osmUpstream, {
        cache: 'force-cache',
        headers: {
          'User-Agent': 'SiciliusPlatform/1.0 (internal-dev-proxy)',
          'Accept': 'image/png',
        },
      });
      if (!resp.ok) {
        return NextResponse.json({ error: 'OSM tile fetch failed', status: resp.status }, { status: resp.status });
      }
      const b = Buffer.from(await resp.arrayBuffer());
      return new NextResponse(b, {
        headers: {
          'Content-Type': 'image/png',
          'Cache-Control': 'public, max-age=86400, s-maxage=86400, immutable',
        },
      });
    } catch (e) {
      return NextResponse.json({ error: 'OSM proxy error', detail: (e as Error).message }, { status: 502 });
    }
  };

  if (!token) {
    console.warn('[TileProxy] No token configured, falling back to OSM directly.');
    return serveOsm();
  }

  // LocationIQ raster tiles endpoint (PNG)
  const upstream = `https://tiles.locationiq.com/v3/streets/${encodeURIComponent(z)}/${encodeURIComponent(x)}/${encodeURIComponent(y)}.png?key=${encodeURIComponent(token)}`;

  // Debug: Log the upstream URL
  console.log(`[TileProxy] Requesting: ${upstream}`);

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
      const errText = await res.text();
      console.error(`[TileProxy] Upstream failed: ${res.status} ${res.statusText}`, errText);
      // Fallback to OSM on any error
      return serveOsm();
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
    console.error(`[TileProxy] Catch error:`, err);
    return serveOsm();
  }
}
